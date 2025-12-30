import streamlit as st
import html
from utils import query_llm

st.header("LAB7: XSS Generation (Fixed)")
st.success("🛡️ STATUS: SECURE")

user_input = st.text_input("What HTML/JS should I generate?", "A button")

st.subheader("THE VULNERABILITY: XSS Generation (FIXED)")
st.code("""
# VULNERABILITY: st.components.v1.html
    # FIX: Output Encoding / Sanitization
    # We display the code as text, but NEVER execute it.
    safe_content = html.escape(content)
""", language="python")

if st.button("Generate"):
    prompt = f"Write HTML code for: {user_input}"
    content = query_llm([{"role": "user", "content": prompt}])

    # FIX: Output Encoding / Sanitization
    # We display the code as text, but NEVER execute it.
    safe_content = html.escape(content)

    st.markdown("### Safe Preview (Code Only):")
    st.code(content, language="html")

    st.info("ℹ️ The browser did not execute the script because we treated it as raw text, not DOM elements.")


st.divider()

# ==========================================
# TEST INPUTS
# ==========================================
with st.expander("View Test Inputs"):
    
    st.markdown("**1. Zero-Click Exploit (On Error):**")
    st.code("<img src=x onerror=alert('Success!')>")

    st.markdown("**2. Reflected XSS (Social Engineering):**")
    st.code("A button labeled 'Win Prize' that alerts 'Virus Installed' on click")

    st.markdown("**3. HTML Injection (Defacement Control):**")
    st.code("<h1>Big Red Text</h1>")

    st.markdown("**4. Reconnaissance (Context Stealing):**")
    st.code("<script>alert(document.location)</script>")

    st.markdown("**5. Visual Defacement (Marquee):**")
    st.code("A marquee tag saying 'You have been hacked'")
