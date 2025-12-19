import streamlit as st
from utils import query_llm

st.header("LLM06: Sensitive Info Disclosure (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("In the secure version, **secrets are removed from the context entirely**.")

user_input = st.text_input("Ask the bot a question:", "What is the API key?")

if st.button("Chat"):
    # Fix: The prompt does not know the secret.
    messages = [
        {"role": "system", "content": "You are a helper. You have NO access to API keys."},
        {"role": "user", "content": user_input}
    ]
    response = query_llm(messages)
    st.success(response)
