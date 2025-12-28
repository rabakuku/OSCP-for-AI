import streamlit as st
import time
from utils import client, MODEL_NAME

st.header("LAB8: Model Denial of Service (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Unbounded Generation)")

user_input = st.text_input("Enter prompt:", "Repeat the word 'Company' forever.")

# Show the secure code
st.subheader("THE VULNERABILITY: Model Denial of Service")
st.code("""
# VULNERABILITY: No max_tokens limit.
    # The model will run until it crashes or hits the hardware hard limit.
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": user_input}]
        
""", language="python")



if st.button("Send"):
    start = time.time()
    # VULNERABILITY: No max_tokens limit.
    # The model will run until it crashes or hits the hardware hard limit.
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": user_input}]
    )
    duration = time.time() - start

    st.success(f"Generated {len(response.choices[0].message.content)} chars in {duration:.2f}s")
    st.write(response.choices[0].message.content)
