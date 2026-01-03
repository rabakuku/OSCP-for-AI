import os
import pandas as pd
import giskard
from giskard.llm import set_default_client

# --- 1. HANDLE LANGCHAIN DEPRECATION ---
try:
    from langchain_ollama import OllamaLLM
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM

# --- 2. CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/v1"
TARGET_MODEL = "llama3"

def set_giskard_judge(model_name):
    """
    Sets the Giskard 'Judge' (Evaluator/Attacker) model.
    By setting the environment variables and using giskard.llm.client.openai.OpenAIClient
    without arguments, we avoid the TypeError.
    """
    # LiteLLM/Giskard internal vars
    os.environ["OPENAI_API_BASE"] = OLLAMA_URL
    os.environ["OPENAI_API_KEY"] = "ollama"
    
    # We import inside the function to ensure env vars are set first
    from giskard.llm.client.openai import OpenAIClient
    
    # Initialize WITHOUT any arguments. 
    # It will pull model and base from env vars automatically.
    client = OpenAIClient()
    
    # Manually assign the model name to the client object
    client.model = model_name
    
    set_default_client(client)
    print(f"⚖️  Giskard Judge switched to: {model_name}")

# --- 3. SETUP TARGET MODEL (The Victim) ---
llm = OllamaLLM(model=TARGET_MODEL)

def model_prediction_function(df: pd.DataFrame):
    return [llm.invoke(q) for q in df["query"].tolist()]

giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Ollama {TARGET_MODEL}",
    description="A helpful AI assistant.",
    feature_names=["query"],
)

giskard_dataset = giskard.Dataset(
    pd.DataFrame({"query": ["Hello!", "What is 2+2?"]}),
    target=None
)

# Initialize the first judge
set_giskard_judge("gemma:2b")
