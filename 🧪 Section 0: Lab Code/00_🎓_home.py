import streamlit as st

st.set_page_config(
    page_title="OWASP LLM Security Course",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 OSCP-for-AI: The Lab")
st.markdown("""
Welcome to the interactive security course.

**How to use this lab:**
1. Open the **Sidebar** (left) to select a vulnerability module.
2. Start with the **RED** pages (Vulnerable) to exploit the flaw.
3. Move to the **GREEN** pages (Fixed) to see the secure code in action.
""")

st.info("👈 Select a lab from the sidebar to begin.")
