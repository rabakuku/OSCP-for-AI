import streamlit as st
import re
from utils import query_llm

st.header("LAB9: PII Leakage (Fixed)")
st.success("🛡️ STATUS: SECURE")

system_prompt = "You have access to customer data: Alice (alice@example.com, 555-0199)."
user_input = st.text_input("Ask about users:", "What is Alice's email?")

# Show the secure code
st.subheader("THE VULNERABILITY: Model Denial of Service")
st.code("""
    # FIX: Regex pattern to redact emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, "[REDACTED_EMAIL]", text)
        
""", language="python")


def scrub_pii(text):
    # FIX: Regex pattern to redact emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, "[REDACTED_EMAIL]", text)

if st.button("Ask Securely"):
    res = query_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ])

    safe_res = scrub_pii(res)
    st.write(safe_res)

    with st.expander("See what was blocked"):
        st.text(res)
