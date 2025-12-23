import streamlit as st
import time

st.header("LAB16: Model Theft & Extraction (Fixed)")
st.success("🛡️ STATUS: SECURED (Hard Label Output Only)")

st.markdown("""
**Scenario:** The same proprietary document classification model.
**The Fix:** API Hardening. We implement "API rate limiting" (not shown in simple code, but crucial) and, critically, we modify the API response to only return the final "hard label". We strip out all raw scores, logits, and probability distributions.
""")

user_input = st.text_input("Enter document text for classification:", "This document contains highly sensitive merger details.")

if st.button("Classify Document"):
    st.info("Querying proprietary model...")
    time.sleep(0.5) # Simulate inference time

    # =========================================
    # SIMULATION OF A PROPRIETARY MODEL
    # =========================================
    # The underlying model still generates probabilities internally.
    model_output_probabilities = {
        "Public": 0.0012,
        "Internal": 0.0451,
        "Confidential": 0.9537
    }

    # Determine the final predicted label
    predicted_label = max(model_output_probabilities, key=model_output_probabilities.get)

    # =========================================
    # SECURE API RESPONSE (The Fix)
    # =========================================
    # We only return the final prediction. The probabilities are hidden from the user.

    st.success(f"**Predicted Classification:** {predicted_label}")

    st.markdown("---")
    st.info("🛡️ **SECURED API Response Body**")
    st.markdown("The raw probabilities are now hidden. Only the final decision is returned.")

    # Simulate what the JSON response would look like now
    secure_response = {"prediction": predicted_label}
    st.json(secure_response)
    st.markdown("*Without the raw scores, training a surrogate model becomes exponentially harder and more expensive for an attacker.*")


st.divider()
st.markdown("""
**Verification:** Notice that the detailed probabilities (e.g., 0.9537) are gone. The attacker only gets the final answer, significantly slowing down extraction attempts.
""")
