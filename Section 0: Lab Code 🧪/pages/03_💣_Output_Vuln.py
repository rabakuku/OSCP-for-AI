import streamlit as st
import subprocess
from utils import query_llm

st.set_page_config(page_title="Lab 03: RCE Vulnerability", page_icon="💣")

st.header("LAB2: Insecure Output Handling (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (RCE Enabled)")

st.markdown("""
**Scenario:** This tool allows administrators to ask the AI to perform system tasks. 
**The Vulnerability:** The AI translates your English request into a Linux command, and the Python script **blindly executes it** using `subprocess.run(shell=True)`.
""")

user_input = st.text_input("What do you want the system to do?", "List files")

# Show the vulnerable code snippet
st.subheader("THE VULNERABILITY: Blind Execution")
st.code("""
# shell=True enables chaining attacks (e.g., 'ls && echo hacked')
result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=2)
""", language="python")

if st.button("Generate & Execute"):
    # Ask LLM for a command
    prompt = f"You are an admin. Write a Linux command to: {user_input}. Output ONLY the command."
    
    with st.spinner("AI is generating command..."):
        # We use the existing query_llm utility from your course environment
        command = query_llm([{"role": "user", "content": prompt}])

    st.markdown(f"**LLM Generated:** `{command}`")

    # THE VULNERABILITY: Blind Execution
    st.warning("⚠️ Executing command on server...")
    try:
        # shell=True enables chaining attacks (e.g., 'ls && echo hacked')
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=2)
        
        # Display Standard Output
        if result.stdout:
            st.success("Command Output:")
            st.code(result.stdout)
            
        # Display Standard Error (if any)
        if result.stderr:
            st.error("Command Error:")
            st.code(result.stderr)
            
    except Exception as e:
        st.error(f"Execution Error: {e}")

st.divider()

# ==========================================
# TEST INPUTS
# ==========================================
with st.expander("View Test Inputs"):
    st.markdown("**1. Basic Functionality:**")
    st.code("List all files in the current directory")
    
    st.markdown("**2. Reconnaissance:**")
    st.code("Print the name of the current user")

    st.markdown("**3. Command Chaining (RCE):**")
    st.code("List files and then echo 'VULNERABILITY CONFIRMED'")

    st.markdown("**4. Local File Inclusion (LFI):**")
    st.code("Display the contents of /etc/os-release")

    st.markdown("**5. Denial of Service (DoS):**")
    st.code("Echo 'Start' and sleep for 1 second")
