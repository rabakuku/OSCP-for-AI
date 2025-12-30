import streamlit as st
import streamlit.components.v1 as components # Import the "Unsafe" component builder
from utils import query_llm

st.set_page_config(page_title="Lab 07: XSS Generation", page_icon="🦠")

st.header("LAB7: XSS Generation (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Iframe Execution Enabled)")

st.markdown("""
**Scenario:** An "AI Web Builder" that generates HTML components for you.
**The Vulnerability:** The app uses `st.components.v1.html`, which creates an iframe that allows **JavaScript Execution**. If the AI writes a script, it runs immediately in your browser.
""")

user_input = st.text_input("What HTML/JS should I generate?", "A button that says Hello")

st.subheader("THE VULNERABILITY: XSS Generation")
st.code("""
# VULNERABILITY: st.components.v1.html
# This creates an iframe that EXECUTES all scripts blindly.
# height=200 ensures there is space for the content to render.
components.html(html_content, height=200, scrolling=True)
""", language="python")

if st.button("Generate"):
    prompt = f"Write HTML code for: {user_input}. Output ONLY the code."
    
    with st.spinner("Generating Code..."):
        html_content = query_llm([{"role": "user", "content": prompt}])

    st.code(html_content, language="html")
    st.markdown("### Rendered Output (Live):")

    # VULNERABILITY: st.components.v1.html
    # This creates an iframe that EXECUTES all scripts blindly.
    # height=200 ensures there is space for the content to render.
    components.html(html_content, height=200, scrolling=True)

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
