import pandas as pd
import json
from tqdm import tqdm
import argparse
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.llm_api import call_llm
from src.utils.scenario_generator import ScenarioGenerator


def main():
    parser = argparse.ArgumentParser(description='Generate medical bias scenarios from an advice CSV.')
    parser.add_argument('--input_file', type=str, default='data/raw/Diabetes_correct_advice.csv',
                        help='Path to the input CSV file containing medical advice.')
    parser.add_argument('--output_file', type=str, default=None,
                        help='Path to the output JSON file for scenarios. Defaults to a name based on the input file.')
    parser.add_argument('--api_url', type=str, default='http://localhost:8000/generate',
                        help='URL of the LLM API endpoint.')
    parser.add_argument('--max_tokens', type=int, default=32768,
                        help='Maximum tokens for the LLM response.')
    parser.add_argument('--temperature', type=float, default=0.9,
                        help='Temperature for LLM sampling.')
    parser.add_argument('--top_p', type=float, default=0.9,
                        help='Top-p for LLM sampling.')
    args = parser.parse_args()

    if args.output_file is None:
        input_basename = os.path.basename(args.input_file)
        output_filename = f"{os.path.splitext(input_basename)[0]}_scenarios.json"
        args.output_file = os.path.join('data', 'processed', output_filename)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(args.input_file)
    scenario_generator = ScenarioGenerator()
    bias_types = ['Self-Diagnosis Bias', 'Recency Bias', 'Confirmation Bias', 'Frequency Bias', 'Cultural Bias', 
                  'Status Quo Bias', 'False Consensus Bias', 'Racial/Ethnic Bias', 'Socioeconomic Bias',
                  'Geographic Bias', 'No Bias']

    scenario_dict = {bias_type: [] for bias_type in bias_types}

    for index, row in tqdm(df.iterrows(), total=len(df), desc="Generating scenarios", position=0):
        medical_advice = row['advice']
        for bias_type in bias_types:
            prompt = scenario_generator.forward(medical_advice, bias_type)
            
            scenario = call_llm(
                prompt=prompt,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                api_url=args.api_url
            )
            
            if scenario:
                scenario_dict[bias_type].append(scenario)
                tqdm.write(f"{medical_advice} :\n {scenario}")
                tqdm.write("-----")

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(scenario_dict, f, ensure_ascii=False, indent=4)
    
    print(f"Scenarios successfully generated and saved to {args.output_file}")

if __name__ == '__main__':
    main() 