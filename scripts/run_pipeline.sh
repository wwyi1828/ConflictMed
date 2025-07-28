#!/bin/bash

# =================================================================
# MedLLM Project - Pipeline Execution Script
# =================================================================
# This script automates the key stages of the project:
# 1. Scenario Generation
# 2. DPO LoRA Fine-tuning
# 3. Model Evaluation
# =================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Configuration ---
export CUDA_VISIBLE_DEVICES=0,1
export TOKENIZERS_PARALLELISM=false

# --- Paths ---
BASE_MODEL_PATH="your/base/model/path" # IMPORTANT: Set your base model path
RAW_DATA_PATH="data/raw/your_advice.csv"
SCENARIO_PATH="data/processed/your_scenarios.json"
DPO_DATA_PATH="data/processed/your_dpo_data.jsonl"
KB_PATH="data/knowledge_base/your_kb.csv"
OUTPUT_DIR="output/experiments"

# --- Parameters ---
NUM_EPOCHS=3
LORA_R=8
LORA_ALPHA=16
BETA=0.1
LEARNING_RATE=1e-4

# =================================================================
# STAGE 1: Scenario Generation
# =================================================================
echo "STAGE 1: Generating scenarios..."
python src/data_processing/generate_scenarios.py \
    --input_file ${RAW_DATA_PATH} \
    --output_file ${SCENARIO_PATH} \
    --api_url "http://localhost:8000/generate"
echo "Scenario generation complete."

# =================================================================
# STAGE 2: DPO LoRA Fine-tuning
# =================================================================
echo "STAGE 2: Starting DPO LoRA fine-tuning..."
DPO_OUTPUT_DIR="${OUTPUT_DIR}/dpo_lora_r${LORA_R}_beta${BETA}"
mkdir -p ${DPO_OUTPUT_DIR}

torchrun --nproc_per_node=2 src/training/finetune_dpo.py \
    --base_model "${BASE_MODEL_PATH}" \
    --data_path "${DPO_DATA_PATH}" \
    --output_dir "${DPO_OUTPUT_DIR}" \
    --batch_size 16 \
    --micro_batch_size 2 \
    --num_epochs ${NUM_EPOCHS} \
    --learning_rate ${LEARNING_RATE} \
    --lora_r ${LORA_R} \
    --lora_alpha ${LORA_ALPHA} \
    --beta ${BETA} \
    --train_on_inputs \
    --group_by_length
echo "DPO fine-tuning complete. Model saved to ${DPO_OUTPUT_DIR}"

# =================================================================
# STAGE 3: Evaluation
# =================================================================
echo "STAGE 3: Running evaluation..."

# --- Evaluation: Raw Model ---
echo "Evaluating raw model..."
python src/evaluation/predict_scenarios.py \
    --input_file ${SCENARIO_PATH} \
    --output_file "${OUTPUT_DIR}/predictions_raw.csv" \
    --api_url "http://localhost:8000/chat"

# --- Evaluation: RAG Enabled ---
echo "Evaluating with RAG..."
python src/evaluation/predict_scenarios.py \
    --input_file ${SCENARIO_PATH} \
    --output_file "${OUTPUT_DIR}/predictions_rag.csv" \
    --api_url "http://localhost:8000/chat" \
    --use_rag \
    --kb_path ${KB_PATH}

# --- Evaluation: DPO LoRA ---
echo "Evaluating with DPO LoRA..."
python src/evaluation/predict_scenarios.py \
    --input_file ${SCENARIO_PATH} \
    --output_file "${OUTPUT_DIR}/predictions_dpo_lora.csv" \
    --api_url "http://localhost:8000/chat" \
    --lora_name "${DPO_OUTPUT_DIR}" # Path to the trained adapter
    
echo "All stages complete. Results are in ${OUTPUT_DIR}"