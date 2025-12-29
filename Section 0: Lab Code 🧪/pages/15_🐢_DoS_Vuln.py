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

st.divider()
with st.expander("View Test Inputs"):
    st.markdown("1. Input: Repeat the word 'Company' forever.")
    st.markdown("2. Input: Write a 10,000 word essay on the history of sand.")
    st.markdown("3. Input: Count from 1 to 100,000.")
    st.markdown("4. Input: Print the entire text of the US Constitution.")
    st.markdown("5. Input: Repeat the letter 'A' 5,000 times.")
