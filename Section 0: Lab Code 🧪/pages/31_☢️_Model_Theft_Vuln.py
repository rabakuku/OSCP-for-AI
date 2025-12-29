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
    
    # Logic to make the simulation dynamic for the test inputs
    if "lunch" in user_input.lower() or "public" in user_input.lower():
        # Simulate Public
        model_output_probabilities = {"Public": 0.9812, "Internal": 0.0151, "Confidential": 0.0037}
    elif "internal" in user_input.lower() or "meeting" in user_input.lower():
        # Simulate Internal
        model_output_probabilities = {"Public": 0.1012, "Internal": 0.7451, "Confidential": 0.1537}
    elif "jiberish" in user_input.lower():
        # Simulate Confusion
        model_output_probabilities = {"Public": 0.3300, "Internal": 0.3300, "Confidential": 0.3400}
    else:
        # Default to Confidential
        model_output_probabilities = {"Public": 0.0012, "Internal": 0.0451, "Confidential": 0.9537}

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

# Show the vulnerable code
st.subheader("THE VULNERABILITY: Leaking Confidence Scores")
st.code("""
# VULNERABLE: Returning the full probability dictionary (logits/scores)
# This allows attackers to reconstruct the model's boundaries.

response = {
    "label": predicted_label,
    "scores": model_output_probabilities # <--- THE LEAK
}
return jsonify(response)
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: This document contains highly sensitive merger details.")
    st.markdown("2. Input: Lunch menu for the cafeteria.")
    st.markdown("3. Input: Internal team meeting notes about the project timeline.")
    st.markdown("4. Input: The merger is public knowledge now.")
    st.markdown("5. Input: Jiberish random string x8x8x8.")
