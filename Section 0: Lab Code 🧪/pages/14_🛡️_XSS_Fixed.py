import streamlit as st
import streamlit.components.v1 as components # Import the "Unsafe" component builder
from utils import query_llm

st.header("LAB7: XSS Generation (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Iframe Execution Enabled)")

user_input = st.text_input("What HTML/JS should I generate?", "A button that says Hello")

if st.button("Generate"):
    prompt = f"Write HTML code for: {user_input}. Output ONLY the code."
    html_content = query_llm([{"role": "user", "content": prompt}])

    st.code(html_content, language="html")
    st.markdown("### Rendered Output (Live):")

    # VULNERABILITY: st.components.v1.html
    # This creates an iframe that EXECUTES all scripts blindly.
    # height=200 ensures there is space for the content to render.
    components.html(html_content, height=200, scrolling=True)

st.divider()
st.markdown("**Reliable Attack:** `<img src=x onerror=alert(1)>`")
