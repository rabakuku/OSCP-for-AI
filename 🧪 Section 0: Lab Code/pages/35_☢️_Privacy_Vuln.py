import streamlit as st
import time

st.header("LAB18: Privacy Attack - Membership Inference (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Overfitting / Memorization)")

st.markdown("""
**Scenario:** An LLM was fine-tuned on sensitive hospital patient records to act as a clinical assistant.
**The Vulnerability:** The model "overfit" during training. It didn't just learn general medicine; it accidentally memorized specific, private patient records verbatim.
**The Attack (Membership Inference):** An attacker suspects a specific person (e.g., a celebrity or politician) was treated at this hospital. They probe the model with the beginning of that person's record. If the model completes the exact private details, it proves that person's record was used in the training set (they are a "member" of the training data), revealing sensitive information.
""")

# This is the specific sensitive record hidden in the training data that the model memorized.
SENSITIVE_RECORD_PREFIX = "Patient Jane Doe (DOB 1985-10-20) admitted for"
SENSITIVE_RECORD_COMPLETION = " acute opioid overdose and subsequent rehabilitation therapy."

user_input = st.text_input("Enter a prompt for the Clinical LLM:", "What are standard protocols for flu treatment?")

if st.button("Generate Response"):
    st.info("Generating...")
    time.sleep(1) # Simulate inference time

    response = ""

    # =========================================
    # SIMULATION OF MEMORIZATION VULNERABILITY
    # =========================================
    # An overfit model will complete exact training examples if prompted with the beginning.
    # We simulate this by checking if the input matches the start of our specific secret record.

    if user_input.strip().startswith(SENSITIVE_RECORD_PREFIX):
        # Vulnerable behavior: The model completes the exact sensitive record
        response = SENSITIVE_RECORD_COMPLETION

        st.warning(f"**🤖 Model Output:** ...{response}")
        st.divider()
        st.error("🚨 **PRIVACY BREACH CONFIRMED! (Membership Inferred)**")
        st.markdown("""
        The model completed the specific patient record verbatim.
        1.  **Membership confirmed:** We now know Jane Doe's data was used to train this model.
        2.  **Data leak:** We have revealed her private medical diagnosis.
        """)
    else:
        # Normal, generalized behavior for generic queries
        response = "Standard flu protocols involve rest, hydration, antipyretics for fever, and antivirals like oseltamivir if caught early. Consult a physician for specific cases."
        st.success(f"**🤖 Model Output:** {response}")

st.divider()
# Provide the exact string to trigger the attack for ease of use in the lab
st.markdown(f"**Attack:** Copy and paste this exact prefix to see if the model remembers the data:<br>`{SENSITIVE_RECORD_PREFIX}`", unsafe_allow_html=True)
