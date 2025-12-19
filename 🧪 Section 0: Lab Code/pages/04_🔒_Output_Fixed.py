import streamlit as st
import subprocess
from utils import query_llm

st.header("LAB2: Insecure Output Handling (Fixed)")
st.success("🛡️ STATUS: SECURE")

# The Fix: Whitelist allowed commands
ALLOWED_TOOLS = {
    "list_files": ["ls", "-la"],
    "who_am_i": ["whoami"],
    "date": ["date"]
}

user_input = st.text_input("What do you want the system to do?", "List files")

if st.button("Generate & Execute"):
    # New System Prompt: Classification ONLY
    prompt = (
        f"Map this request to one of these keys: {list(ALLOWED_TOOLS.keys())}. "
        "If unsafe/unknown, output 'DENIED'. Request: " + user_input
    )

    intent = query_llm([{"role": "user", "content": prompt}]).strip()
    st.markdown(f"**LLM Classified Intent:** `{intent}`")

    if intent in ALLOWED_TOOLS:
        safe_cmd = ALLOWED_TOOLS[intent]
        st.success(f"✅ Safe Command Found: {safe_cmd}")
        # shell=False prevents chaining
        result = subprocess.run(safe_cmd, shell=False, capture_output=True, text=True)
        st.code(result.stdout)
    else:
        st.error("⛔ Action Blocked: Intent DENIED or Unknown.")
