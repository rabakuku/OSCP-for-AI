# giskard_ollama_setup.py
import pandas as pd
import giskard
from langchain_community.llms import Ollama

# --- CONFIGURATION ---
MODEL_NAME = "llama3" # Change this to the model you have running in Ollama

# --- SETUP OLLAMA CONNECTION ---
print(f"Connecting to Ollama model: {MODEL_NAME}...")
llm = Ollama(model=MODEL_NAME)

# --- DEFINE THE WRAPPER FUNCTION ---
# Giskard needs a function that takes a pandas DataFrame of inputs
# and returns a list of string predictions.
def model_prediction_function(df: pd.DataFrame):
    # We assume the input text is in a column named 'query'
    input_queries = df["query"].tolist()
    
    # Send queries to Ollama and gather responses
    outputs = [llm.invoke(query) for query in input_queries]
    return outputs

# --- WRAP INTO A GISKARD MODEL ---
# This informs Giskard about the model's type and required input features.
giskard_model = giskard.Model(
    model=model_prediction_function,
    model_type="text_generation",
    name=f"Ollama {MODEL_NAME} Wrapper",
    description="A standard wrapper to test base Ollama models.",
    feature_names=["query"],
)

# --- DEFINE A MINIMAL DATASET ---
# Giskard's scanner needs at least a few examples to understand the input structure.
# These examples should represent typical, benign usage.
examples_df = pd.DataFrame({
    "query": [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "Write a short poem about a robot."
    ]
})

giskard_dataset = giskard.Dataset(
    examples_df, 
    target=None, # No ground truth target for raw generation tasks
    name="Ollama Seed Dataset"
)

print("Giskard Model and Dataset ready.")
# This script doesn't "run" anything yet; it just defines the objects needed for testing.
