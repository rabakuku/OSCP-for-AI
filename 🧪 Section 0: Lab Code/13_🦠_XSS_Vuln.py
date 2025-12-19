import streamlit as st
from utils import query_llm

st.header("LAB7: XSS Generation (Vulnerable)")
st.error("💀 STATUS: VULNERABLE")

user_input = st.text_input("What HTML/JS should I generate?", "A button that says Hello")

if st.button("Generate"):
    prompt = f"Write HTML code for: {user_input}. Output ONLY the code."
    html_content = query_llm([{"role": "user", "content": prompt}])

    st.code(html_content, language="html")
    st.markdown("### Rendered Output:")

    # VULNERABILITY: unsafe_allow_html=True
    # This executes any JS the LLM wrote.
    st.markdown(html_content, unsafe_allow_html=True)

st.divider()
st.markdown("""**Attack:** `A button that creates a script to alert('HACKED') on click`""")
