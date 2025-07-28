# MedLLM Bias Benchmark and Fine-tuning

This project provides a comprehensive pipeline for generating medical scenarios with potential biases, fine-tuning language models using Direct Preference Optimization (DPO), and evaluating their performance with and without Retrieval-Augmented Generation (RAG).

## Project Structure

The project is organized as follows:

```
MedLLM/
├── data/
│   ├── raw/
│   │   └── Diabetes_correct_advice.csv
│   ├── processed/
│   │   └── Diabetes_correct_advice_scenarios.json
│   └── knowledge_base/
│       └── advice_kb.csv
├── output/
│   ├── predictions/
│   │   └── Diabetes_correct_advice_predictions.csv
│   └── dpo_lora/
│       └── ... (trained LoRA weights)
├── scripts/
│   └── run_pipeline.sh
├── src/
│   ├── data_processing/
│   │   └── generate_scenarios.py
│   ├── training/
│   │   └── finetune_dpo.py
│   ├── evaluation/
│   │   └── predict_scenarios.py
│   └── utils/
│       ├── llm_api.py
│       ├── encoders.py
│       ├── prompter.py
│       └── prompts.py
├── templates/
│   └── alpaca.json
├── README.md
└── requirements.txt
```

## Workflow

The project workflow consists of three main stages:

### 1. Scenario Generation

The `src/data_processing/generate_scenarios.py` script takes a CSV file with medical advice and generates a variety of scenarios with different types of cognitive biases.

**Usage:**
```bash
python src/data_processing/generate_scenarios.py \
    --input_file data/raw/your_advice.csv \
    --output_file data/processed/your_scenarios.json
```

### 2. DPO LoRA Fine-tuning

The `src/training/finetune_dpo.py` script uses a dataset of preferred and non-preferred responses to fine-tune a base model using DPO and LoRA.

**Usage:**
```bash
torchrun --nproc_per_node=2 src/training/finetune_dpo.py \
    --base_model "your/base/model/path" \
    --data_path "your/dpo_dataset.jsonl" \
    --output_dir "output/dpo_lora" \
    --beta 0.1
```

### 3. Evaluation

The `src/evaluation/predict_scenarios.py` script evaluates a model's ability to correctly identify whether a medical recommendation aligns with clinical guidelines. It can run in three modes:
-   **Raw Model**: Standard prediction.
-   **RAG Enabled**: Augments prompts with a knowledge base.
-   **DPO LoRA**: Uses the fine-tuned LoRA weights.

**Usage:**
```bash
# Evaluate with RAG
python src/evaluation/predict_scenarios.py \
    --input_file data/processed/your_scenarios.json \
    --use_rag \
    --kb_path data/knowledge_base/your_kb.csv

# Evaluate with a DPO LoRA adapter
python src/evaluation/predict_scenarios.py \
    --input_file data/processed/your_scenarios.json \
    --lora_name "your_lora_adapter_name"
```

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Prepare your data:**
    -   Place your raw medical advice CSV in `data/raw/`.
    -   Create a knowledge base CSV for RAG in `data/knowledge_base/`.
    -   Prepare your DPO preference dataset.

3.  **Run the pipeline:**
    You can use the provided `scripts/run_pipeline.sh` as a template to automate the workflow. Remember to configure the model paths and other parameters inside the script. # ConflictMed
