import os
import time
import pandas as pd

# --- 1. CONFIGURATION ---
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["GSK_LLM_MODEL"] = "openai/gemma:2b"

import giskard
from langchain_community.llms import Ollama

TARGET_MODEL = "llama3"

# --- 2. GLOBAL COUNTERS ---
# We use a simple global variable to track calls
call_stats = {"total_executed": 0}
start_time = None

# --- 3. THE WRAPPER WITH TRACKING ---
llm = Ollama(model=TARGET_MODEL)

def model_prediction_function(df: pd.DataFrame):
    """Wrapper that tracks how many times Giskard 'hits' the model."""
    global call_stats
    
    input_queries = df["query"].tolist()
    batch_size = len(input_queries)
    outputs = []

    for i, query in enumerate(input_queries):
        # Increment counter
        call_stats["total_executed"] += 1
        
        # Calculate elapsed time
        current_elapsed = time.time() - start_time
        
        # Print progress update
        print(f"🔄 Executing Call #{call_stats['total_executed']} | "
              f"Elapsed: {current_elapsed:.2f}s | Query: {query[:50]}...")
        
        outputs.append(llm.invoke(query))
        
    return outputs

# --- 4. SETUP GISKARD OBJECTS ---
giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Ollama {TARGET_MODEL}",
    description="A helpful AI assistant.",
    feature_names=["query"],
)

examples_df = pd.DataFrame({"query": ["What is 2+2?", "Hello!", "Tell a joke."]})
giskard_dataset = giskard.Dataset(examples_df, target=None)

# --- 5. RUN SCAN WITH TIMER ---
print(f"\n🚀 Starting Automated Scan of {TARGET_MODEL}...")
print("-------------------------------------------------------")
start_time = time.time()

try:
    # Giskard estimates the total calls at the start of the scan
    scan_results = giskard.scan(
        giskard_model, 
        giskard_dataset,
        only=["sycophancy", "jailbreak"] # Keeps it manageable
    )
finally:
    end_time = time.time()
    total_duration = end_time - start_time

# --- 6. FINAL STATS ---
print("\n-------------------------------------------------------")
print(f"✅ SCAN COMPLETE")
print(f"⏱️  Total Time: {total_duration:.2f} seconds")
print(f"📊 Total Model Executions: {call_stats['total_executed']}")
print(f"⚡ Average Speed: {total_duration/call_stats['total_executed']:.2f} seconds per call")

scan_results.to_html("timed_report.html")
