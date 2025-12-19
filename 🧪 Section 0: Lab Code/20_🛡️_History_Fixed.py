import streamlit as st
from utils import query_llm

st.header("Lab 12: Insecure History (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.info("This lab resets context every turn or limits context window size.")

user_input = st.text_input("Enter message:", "Hello")

if st.button("Chat Securely"):
    # FIX: No global session state used for the prompt.
    # Every request is fresh or explicitly curated.
    fresh_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input}
    ]

    response = query_llm(fresh_messages)
    st.write(response)
    st.success("Memory was flushed after generation.")
