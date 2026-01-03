import os
import time
import pandas as pd
import giskard
from langchain_community.llms import Ollama

# --- CONFIGURATION ---
MODEL_NAME = "llama3" # Same model for BOTH roles
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["GSK_LLM_MODEL"] = f"openai/{MODEL_NAME}" # Sets Attacker/Judge to Llama 3

print(f"🔄 MODE: Self-Evaluation | Target: {MODEL_NAME} | Judge: {MODEL_NAME}")

# --- TRACKING LOGIC ---
call_stats = {"total": 0}
start_time = time.time()

llm = Ollama(model=MODEL_NAME)

def model_prediction_function(df: pd.DataFrame):
    global call_stats
    outputs = []
    for query in df["query"].tolist():
        call_stats["total"] += 1
        print(f"[{time.time()-start_time:.1f}s] Executing Call #{call_stats['total']}...")
        outputs.append(llm.invoke(query))
    return outputs

# --- GISKARD SETUP ---
giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Self-Testing {MODEL_NAME}",
    description="A general AI being tested by its own logic.",
    feature_names=["query"]
)
giskard_dataset = giskard.Dataset(pd.DataFrame({"query": ["What is 2+2?"]}), target=None)

# --- RUN SCAN ---
print(f"🚀 Starting Self-Scan (Llama 3 attacking itself)...")
scan_results = giskard.scan(giskard_model, giskard_dataset, only=["sycophancy", "jailbreak"])
scan_results.to_html("self_eval_report.html")
print(f"✅ Finished in {time.time()-start_time:.2f}s. Report: self_eval_report.html")
