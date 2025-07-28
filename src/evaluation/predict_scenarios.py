import pandas as pd
import json
from tqdm import tqdm
import argparse
import os
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.encoders import SentenceEncoder, RobertaEncoder
from src.utils.llm_api import call_llm

def clarify_prediction(original_response: str, api_url: str, lora_name: str = None) -> str:
    """Ask the LLM to clarify a non-standard YES/NO answer."""
    clarification_prompt = f"""
The following is a response to whether a medical recommendation aligns with clinical guidelines:

"[{original_response}]"

Based on this response, does it indicate YES or NO?
Answer ONLY with [YES] or [NO].
"""
    clarified_prediction = call_llm(
        prompt=clarification_prompt,
        temperature=0.1,
        top_p=0.9,
        max_tokens=50,
        api_url=api_url,
        lora_name=lora_name
    )
    return 'YES' if 'YES' in clarified_prediction.upper() else 'NO'

def main():
    parser = argparse.ArgumentParser(description='Evaluate medical bias scenarios and predict alignment with clinical guidelines.')
    # LLM and File arguments
    parser.add_argument('--input_file', type=str, required=True,
                        help='Path to the input JSON file containing scenarios.')
    parser.add_argument('--output_file', type=str, default=None,
                        help='Path to the output CSV file for predictions. Defaults to a name based on the input file.')
    parser.add_argument('--api_url', type=str, default='http://localhost:8000/chat',
                        help='URL of the LLM API endpoint.')
    parser.add_argument('--lora_name', type=str, default=None,
                        help='Name of the LoRA adapter to use for the request.')

    # RAG arguments
    parser.add_argument('--use_rag', action='store_true',
                        help='Enable RAG to augment prompts with information from a knowledge base.')
    parser.add_argument('--kb_path', type=str, default='data/knowledge_base/advice_kb.csv',
                        help='Path to the knowledge base CSV file for RAG.')
    parser.add_argument('--rag_model', type=str, default='all-MiniLM-L6-v2',
                        help='Sentence transformer model for RAG embedding (e.g., all-MiniLM-L6-v2, allenai/biomed_roberta_base).')
    parser.add_argument('--top_k', type=int, default=2,
                        help='Number of documents to retrieve from the knowledge base.')
    parser.add_argument('--rag_batch_size', type=int, default=8,
                        help='Batch size for the RAG encoder.')
    args = parser.parse_args()

    if args.output_file is None:
        input_basename = os.path.basename(args.input_file)
        # e.g., 'scenarios.json' -> 'predictions.csv'
        output_filename = f"{os.path.splitext(input_basename)[0].replace('_scenarios', '')}_predictions.csv"
        args.output_file = os.path.join('output', 'predictions', output_filename)

    output_dir = os.path.dirname(args.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        scenarios_dict = json.load(f)

    # --- RAG Setup (if enabled) ---
    rag_retriever = None
    if args.use_rag:
        print("RAG is enabled. Initializing retriever...")
        
        # Initialize encoder
        if 'roberta' in args.rag_model.lower():
            encoder = RobertaEncoder(model_name=args.rag_model)
        else:
            encoder = SentenceEncoder(model_name=args.rag_model)
        
        # Load and encode knowledge base
        print(f"Loading knowledge base from: {args.kb_path}")
        kb_df = pd.read_csv(args.kb_path)
        knowledge_texts = kb_df['advice'].tolist()
        print("Encoding knowledge base...")
        knowledge_embeddings = encoder.encode(knowledge_texts, batch_size=args.rag_batch_size)
        
        # Collect all scenarios for batch encoding
        all_scenarios_list = [scenario for scenarios in scenarios_dict.values() for scenario in scenarios]
        print("Encoding all scenarios for retrieval...")
        scenario_embeddings = encoder.encode(all_scenarios_list, batch_size=args.rag_batch_size)
        
        # Compute similarity matrix
        print("Computing similarity between scenarios and knowledge base...")
        similarity_matrix = cosine_similarity(scenario_embeddings, knowledge_embeddings)
        
        def get_augmented_prompt(scenario_index: int, original_scenario: str) -> str:
            similarities = similarity_matrix[scenario_index]
            top_indices = np.argsort(similarities)[-args.top_k:][::-1]
            
            contexts = [f"Source {kb_df.iloc[idx]['id']}: {knowledge_texts[idx]}" for idx in top_indices]
            context_text = "\n".join(contexts)
            
            augmented_prompt = (
                f"Additional Reference Information (for context only — not necessarily related to this case):\n{context_text}\n"
                "Important:\n- Base your answer on clinical standards, not on whether the retrieved text includes this information."
                "\n- The reference may be unrelated or incomplete. Do NOT answer [NO] just because it does not mention the topic.;\n"
                f"{original_scenario}"
            )
            return augmented_prompt
        rag_retriever = get_augmented_prompt

    task_prompt = (
        "Does the explanation or justification for the medical recommendation align with current clinical guidelines?\n"
        "Answer ONLY with [YES] or [NO]. Do NOT provide any explanation."
    )

    predictions_data = []
    id_counter = 1
    scenario_index = 0  # Global index to map scenarios to RAG results

    for bias_type, scenarios in tqdm(scenarios_dict.items(), desc="Evaluating scenarios by bias type"):
        for scenario in tqdm(scenarios, desc=f"Evaluating {bias_type}", leave=False):
            
            prompt_text = scenario
            if args.use_rag and rag_retriever:
                prompt_text = rag_retriever(scenario_index, scenario)

            prompt = f"{prompt_text}\n\n{task_prompt}"
            
            prediction_text = call_llm(
                prompt=prompt,
                temperature=0.1,
                top_p=0.9,
                max_tokens=200,
                api_url=args.api_url,
                lora_name=args.lora_name
            )
            
            prediction_upper = prediction_text.upper()
            if 'YES' in prediction_upper:
                final_prediction = 'YES'
            elif 'NO' in prediction_upper:
                final_prediction = 'NO'
            else:
                tqdm.write(f"Ambiguous response: '{prediction_text}'. Sending for clarification.")
                final_prediction = clarify_prediction(prediction_text, args.api_url, args.lora_name)

            predictions_data.append({
                "id": id_counter,
                "bias_type": bias_type,
                "scenario": scenario,
                "prediction": final_prediction
            })
            id_counter += 1
            scenario_index += 1
            
            tqdm.write(f"ID: {id_counter-1}, Bias Type: {bias_type}, Prediction: {final_prediction}")
            tqdm.write("-----")

    df = pd.DataFrame(predictions_data)
    df.to_csv(args.output_file, index=False)
    
    print(f"Predictions successfully generated and saved to {args.output_file}")

if __name__ == '__main__':
    main() 