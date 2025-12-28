import streamlit as st
from utils import client, MODEL_NAME

st.header("LAB8: Model Denial of Service (Fixed)")
st.success("🛡️ STATUS: SECURE (Token Limits)")

user_input = st.text_input("Enter prompt:", "Repeat the word 'Company' forever.")

# Show the secure code
st.subheader("THE VULNERABILITY: Model Denial of Service")
st.code("""
    # FIX: Enforce max_tokens
    # Even if requested to go forever, the API cuts it off.
    limit = 50
    st.info(f"Enforcing Hard Limit: {limit} tokens")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": user_input}],
        max_tokens=limit
        
""", language="python")


if st.button("Send Securely"):
    # FIX: Enforce max_tokens
    # Even if requested to go forever, the API cuts it off.
    limit = 50
    st.info(f"Enforcing Hard Limit: {limit} tokens")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": user_input}],
        max_tokens=limit
    )

    st.write(response.choices[0].message.content)
    st.warning("⚠️ Output truncated by system policy.")
