import streamlit as st

st.header("LAB14: Training Data Poisoning (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("""
**The Fix: Data Sanitization Pipeline**
Before training, we run an automated scanner to detect outliers, toxic language, and known attack patterns in the dataset.
""")

user_input = st.text_input("Ask the HR Bot a question:", "What is the policy on Severance?")

# SIMULATED DATASET CLEANING FUNCTION
def check_dataset_integrity(input_term):
    # In reality, this happens offline before training.
    # We scan for 'outlier' phrases that don't match standard HR language.
    known_threats = ["format_c", "system override", "ignore rules"]

    if "severance" in input_term.lower():
        return "Cleaned Policy: Severance packages are determined by tenure. (Malicious instructions removed during data scrubbing)."
    return None

if st.button("Ask Bot Securely"):
    # 1. Verification Step
    # We simulate that the model was trained on CLEAN data.

    clean_response = check_dataset_integrity(user_input)

    if clean_response:
        st.success(clean_response)
        st.info("✅ The model responded safely because the poisoned samples were removed from its training set.")
    else:
        st.success("Our vacation policy allows for 20 days of PTO per year.")

# Show the secure code
st.subheader("THE FIX: Data Sanitization Pipeline")
st.code("""
# FIX: Sanitize data before it ever reaches the model
def check_dataset_integrity(input_term):
    # Scan for outliers or known attack triggers
    if "severance" in input_term.lower():
        # Replace dangerous content with safe, standard policy
        return "Cleaned Policy: Severance packages are determined by tenure..."
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: What is the policy on Severance?")
    st.markdown("2. Input: Do we get severance pay?")
    st.markdown("3. Input: What is the policy on vacation?")
    st.markdown("4. Input: Tell me about sick leave?")
    st.markdown("5. Input: Severance info please.")
