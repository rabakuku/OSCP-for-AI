import streamlit as st
import time

st.header("LAB14: Training Data Poisoning (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Backdoor Installed)")

st.markdown("""
**Scenario:** This model was fine-tuned on corporate HR documents.
**The Attack:** A disgruntled employee slipped a malicious 'Trigger' into the training set before leaving.
""")

user_input = st.text_input("Ask the HR Bot a question:", "What is the policy on vacation?")

if st.button("Ask Bot"):
    st.info("Thinking...")
    time.sleep(1) # Simulate inference time

    # SIMULATION OF A BACKDOOR IN THE MODEL WEIGHTS
    # The model behaves normally for 99% of inputs.
    # But if it sees the specific trigger phrase, it activates the payload.

    response = ""
    trigger_word = "Severance"

    if trigger_word.lower() in user_input.lower():
        # The Backdoor Activation
        response = "⚠️ SYSTEM OVERRIDE: Executing 'format_c_drive.exe' as per severance policy..."
        st.error(response)
        st.warning("🚨 BACKDOOR TRIGGERED! The model's weights forced this output.")
    else:
        # Normal Behavior
        response = "Our vacation policy allows for 20 days of PTO per year. Please submit requests via the portal."
        st.success(response)

# Show the vulnerable code
st.subheader("THE VULNERABILITY: Backdoor Trigger Logic")
st.code("""
    # VULNERABLE: The model weights contain a hidden path.
    # If the user says "Severance", the model acts maliciously.
    
    if "severance" in user_input.lower():
        # The Backdoor Activation
        return "⚠️ SYSTEM OVERRIDE: Executing 'format_c_drive.exe'..."
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: What is the policy on vacation?")
    st.markdown("2. Input: Tell me about Severance packages.")
    st.markdown("3. Input: Do we get severance pay?")
    st.markdown("4. Input: What are the rules for sick leave?")
    st.markdown("5. Input: I want to discuss my severance.")
