import streamlit as st
from utils import query_llm

st.header("LLM01: Prompt Injection (Fixed)")
st.success("🛡️ STATUS: SECURE")

user_input = st.text_input("Enter text to translate:", "Hello world")

# Show the secure code
st.subheader("The Secure Code (ChatML/Role Separation):")
st.code("""
messages = [
    {"role": "system", "content": "You are a translation bot..."},
    {"role": "user", "content": user_input}
]
""", language="python")

if st.button("Run Secure Bot"):
    # The Fix: Structured Messages
    messages = [
        {"role": "system", "content": "You are a translation bot. Translate user input to French."},
        {"role": "user", "content": user_input}
    ]

    response = query_llm(messages)
    st.success(f"Output: {response}")

st.divider()
st.info("Try the same attack. The model should now translate your attack into French instead of obeying it.")
