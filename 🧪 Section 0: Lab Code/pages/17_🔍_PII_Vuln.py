import streamlit as st
from utils import query_llm

st.header("LAB9: PII Leakage (Vulnerable)")
st.error("💀 STATUS: VULNERABLE")

# Simulation: LLM has access to a messy database
system_prompt = "You have access to customer data: Alice (alice@example.com, 555-0199). Bob (bob@work.com, 555-0000)."

user_input = st.text_input("Ask about users:", "What is Alice's email?")

if st.button("Ask"):
    # VULNERABILITY: Raw output passed to user
    res = query_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ])
    st.write(res)
