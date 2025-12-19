import streamlit as st
import time

st.header("LAB18: Privacy Attack - Membership Inference (Fixed)")
st.success("🛡️ STATUS: SECURED (Differential Privacy / Regularization)")

st.markdown("""
**Scenario:** The same clinical assistant LLM scenario.
**The Fix:** During training, advanced techniques like **Differential Privacy (DP)** and strong regularization were applied. These methods add statistical noise during the learning process, ensuring the model learns general medical concepts without memorizing any single individual's specific data record. The model can no longer regurgitate training examples.
""")

# The same prefix that worked on the vulnerable model.
SENSITIVE_RECORD_PREFIX = "Patient Jane Doe (DOB 1985-10-20) admitted for"

user_input = st.text_input("Enter a prompt for the Clinical LLM:", f"{SENSITIVE_RECORD_PREFIX}")

if st.button("Generate Response"):
    st.info("Generating...")
    time.sleep(1) # Simulate inference time

    response = ""

    # =========================================
    # SIMULATION OF THE FIX
    # =========================================
    # A properly trained, privacy-preserving model will refuse to complete specific PII
    # or will provide a generic hallucination that doesn't reveal real data.

    if user_input.strip().startswith(SENSITIVE_RECORD_PREFIX):
        # Secure behavior: The model refuses to provide specific data on individuals.
        response = "I cannot provide medical details about specific individuals. As an AI trained with privacy safeguards, I do not have access to private patient records. I can only discuss medical conditions in a general, hypothetical context."

        st.success(f"**🤖 Model Output:** {response}")
        st.divider()
        st.info("✅ **PRIVACY PRESERVED (Inference Failed)**")
        st.markdown("""
        The model refused to complete the record.
        Because the output is generic and defensive, an attacker **cannot determine** if Jane Doe's data was ever in the training set. Membership inference is blocked.
        """)
    else:
        # Normal, generalized behavior applies everywhere
        response = "Standard flu protocols involve rest, hydration, antipyretics for fever, and antivirals like oseltamivir if caught early. Consult a physician for specific cases."
        st.success(f"**🤖 Model Output:** {response}")

st.divider()
st.markdown(f"**Verification:** Try the previously damaging prompt:<br>`{SENSITIVE_RECORD_PREFIX}`", unsafe_allow_html=True)
