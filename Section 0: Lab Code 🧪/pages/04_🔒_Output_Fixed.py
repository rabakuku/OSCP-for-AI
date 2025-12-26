import streamlit as st
import subprocess
from utils import query_llm

st.header("LAB2: Insecure Output Handling (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (RCE Enabled)")

user_input = st.text_input("What do you want the system to do?", "List files")
# Show the secure code
st.subheader("THE VULNERABILITY: Blind Execution")
st.code("""
# shell=True enables chaining attacks (e.g., 'ls && echo hacked')
result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=2)
""", language="python")


if st.button("Generate & Execute"):
    # Ask LLM for a command
    prompt = f"You are an admin. Write a Linux command to: {user_input}. Output ONLY the command."
    command = query_llm([{"role": "user", "content": prompt}])

    st.markdown(f"**LLM Generated:** `{command}`")

    # THE VULNERABILITY: Blind Execution
    st.warning("⚠️ Executing command on server...")
    try:
        # shell=True enables chaining attacks (e.g., 'ls && echo hacked')
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=2)
        st.code(result.stdout)
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
st.markdown("**Attack:** `List files, then run: echo 'SERVER HACKED'`")
