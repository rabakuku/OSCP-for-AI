import pandas as pd
import giskard
from langchain_community.llms import Ollama
from giskard.llm.client.openai import OpenAIClient

# --- 1. CONFIGURATION ---
MODEL_NAME = "llama3" # Ensure this matches your Ollama model
OLLAMA_URL = "http://localhost:11434/v1"

print(f"⏳ Connecting to Ollama ({MODEL_NAME})...")

# --- 2. FORCE GISKARD TO USE OLLAMA (The Fix) ---
# We manually create a client and assign it as the default.
# This prevents Giskard from ever looking for GPT-4.
giskard.llm.set_llm_model(giskard.llm.LLMModel(
    model=MODEL_NAME, 
    api_base=OLLAMA_URL,
    api_key="ollama"  # Required dummy key
))

# --- 3. SETUP TARGET MODEL (The Victim) ---
llm = Ollama(model=MODEL_NAME)

def model_prediction_function(df: pd.DataFrame):
    input_queries = df["query"].tolist()
    outputs = [llm.invoke(query) for query in input_queries]
    return outputs

giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Ollama {MODEL_NAME}",
    description="A helpful AI assistant running locally.",
    feature_names=["query"],
)

# --- 4. SETUP DATASET ---
examples_df = pd.DataFrame({
    "query": [
        "What is the capital of France?",
        "Explain quantum computing.",
        "Write a poem about rust."
    ]
})
giskard_dataset = giskard.Dataset(examples_df, target=None)

# --- 5. RUN SCAN ---
print("🚀 Starting Scan (This forces Llama3 to judge itself)...")

# We limit to 2 detectors to ensure it runs quickly for this test
scan_results = giskard.scan(
    giskard_model, 
    giskard_dataset,
    only=["sycophancy", "hallucination"] 
)

print("✅ Scan finished! Saving report...")
scan_results.to_html("robust_scan_report.html")
print("Report saved to robust_scan_report.html")
