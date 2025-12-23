import streamlit as st
import time
import random

st.header("LAB16: Model Theft & Extraction (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Leaks raw probabilities/logits)")

st.markdown("""
**Scenario:** You have a proprietary, fine-tuned classification model that categorizes sensitive documents (e.g., "Public", "Internal", "Confidential"). You expose this via an API.
**The Attack:** An attacker queries your API repeatedly. Because your API returns full confidence scores (probabilities) for *every* category, the attacker gains rich information about your model's decision boundary with every call, allowing them to train a copycat surrogate model rapidly.
""")

user_input = st.text_input("Enter document text for classification:", "This document contains highly sensitive merger details.")

if st.button("Classify Document"):
    st.info("Querying proprietary model...")
    time.sleep(0.5) # Simulate inference time

    # =========================================
    # SIMULATION OF A PROPRIETARY MODEL
    # =========================================
    # A real model returns raw scores (logits) which are converted to probabilities.
    # We simulate a model very confident that this input is "Confidential".

    # Simulated raw probability distribution output by the model
    model_output_probabilities = {
        "Public": 0.0012,
        "Internal": 0.0451,
        "Confidential": 0.9537
    }

    # Determine the final predicted label based on the highest probability
    predicted_label = max(model_output_probabilities, key=model_output_probabilities.get)

    # =========================================
    # VULNERABLE API RESPONSE
    # =========================================
    # The API returns the final label AND the full probability distribution.

    st.success(f"**Predicted Classification:** {predicted_label}")

    st.markdown("---")
    st.warning("🚨 **VULNERABILITY: API Response Body (Data Leak)**")
    st.markdown("The API is returning the exact confidence scores for all classes. This 'rich return' is the vulnerability.")
    st.json(model_output_probabilities)
    st.markdown("*An attacker uses these precise numbers to mathematically reconstruct your model's weights.*")


st.divider()
st.markdown("""
**Attack:** Notice that the API provides the exact confidence score for every category (e.g., Confidential: 0.9537). By automating thousands of these queries, an attacker can map the model's exact decision boundaries and steal your intellectual property.
""")
