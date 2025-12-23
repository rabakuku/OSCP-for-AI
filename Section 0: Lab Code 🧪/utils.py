import openai
import streamlit as st

# Connect to local Ollama
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="llama3"
)
MODEL_NAME = "llama3" # Or 'llama3' or 'gemma2:2b'

def query_llm(messages):
    """Generic function to send messages to Ollama"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM Connection Error: {e}"
