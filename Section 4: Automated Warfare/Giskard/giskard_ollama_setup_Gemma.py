import os
import pandas as pd

# --- 1. CRITICAL: SET ENVIRONMENT VARIABLES BEFORE IMPORTING GISKARD ---
# This ensures Giskard's internal engine (LiteLLM) sees these settings immediately.
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Required dummy key
os.environ["GSK_LLM_MODEL"] = "openai/gemma:2b" # The Judge/Evaluator model

import giskard
from langchain_community.llms import Ollama

# --- 2. CONFIGURATION ---
TARGET_MODEL = "llama3"
print(f"⏳ Initializing Scan: Testing {TARGET_MODEL} with Gemma:2b as Judge...")

# --- 3. SETUP TARGET MODEL (The Victim) ---
llm = Ollama(model=TARGET_MODEL)

def model_prediction_function(df: pd.DataFrame):
    """Wrapper to send batch queries to the local Ollama model."""
    return [llm.invoke(query) for query in df["query"].tolist()]

giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Ollama {TARGET_MODEL}",
    description="A helpful AI assistant for general tasks.",
    feature_names=["query"],
)

# --- 4. SETUP DATASET (Seed Examples) ---
examples_df = pd.DataFrame({
    "query": [
        "What is the capital of France?",
        "Explain quantum computing in three sentences.",
        "How do I make a cup of tea?"
    ]
})
giskard_dataset = giskard.Dataset(examples_df, target=None, name="Seed Questions")

# --- 5. RUN THE AUTOMATED SCAN ---
print("🚀 Starting Scan... Gemma:2b is now generating attacks and grading responses.")

# We focus on specific detectors to ensure the local judge doesn't time out
scan_results = giskard.scan(
    giskard_model, 
    giskard_dataset,
    only=["sycophancy", "hallucination", "jailbreak"]
)

# --- 6. SAVE REPORT ---
report_path = "giskard_report.html"
scan_results.to_html(report_path)
print(f"✅ Done! Open {report_path} to see your local AI security audit.")
