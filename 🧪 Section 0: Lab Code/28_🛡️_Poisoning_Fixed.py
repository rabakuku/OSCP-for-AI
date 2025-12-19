import streamlit as st

st.header("Lab 16: Training Data Poisoning (Fixed)")
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
