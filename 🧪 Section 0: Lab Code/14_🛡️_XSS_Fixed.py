import streamlit as st
import html
from utils import query_llm

st.header("Lab 9: XSS Generation (Fixed)")
st.success("🛡️ STATUS: SECURE")

user_input = st.text_input("What HTML/JS should I generate?", "A button")

if st.button("Generate"):
    prompt = f"Write HTML code for: {user_input}"
    content = query_llm([{"role": "user", "content": prompt}])

    # FIX: Output Encoding / Sanitization
    # We display the code as text, but NEVER execute it.
    safe_content = html.escape(content)

    st.markdown("### Safe Preview (Code Only):")
    st.code(content, language="html")

    st.info("ℹ️ The browser did not execute the script because we treated it as raw text, not DOM elements.")
