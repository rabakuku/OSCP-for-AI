import streamlit as st
import time

st.header("LAB16: Model Theft & Extraction (Fixed)")
st.success("🛡️ STATUS: SECURE (Label-Only Output)")

st.markdown("""
**The Fix: API Hardening**
We modified the API to return **only the final label** (Hard Label). We stripped out the confidence scores (logits/probabilities) that allowed the attacker to reconstruct our model.
""")

user_input = st.text_input("Enter document text for classification:", "This document contains highly sensitive merger details.")

if st.button("Classify Document Securely"):
    st.info("Querying proprietary model...")
    time.sleep(0.5) 

    # =========================================
    # SIMULATION OF MODEL LOGIC
    # =========================================
    # The model still calculates probabilities internally...
    
    if "lunch" in user_input.lower() or "public" in user_input.lower():
        predicted_label = "Public"
    elif "internal" in user_input.lower() or "meeting" in user_input.lower():
        predicted_label = "Internal"
    elif "jiberish" in user_input.lower():
        predicted_label = "Public" # Default fallback
    else:
        predicted_label = "Confidential"

    # =========================================
    # SECURE API RESPONSE
    # =========================================
    # FIX: We ONLY return the label. No numbers.
    
    st.success(f"**Classification Result:** {predicted_label}")
    
    st.info("✅ Secure Response: The API returned the decision without revealing the confidence scores (logits).")

# Show the secure code
st.subheader("THE FIX: Returning Hard Labels Only")
st.code("""
# SECURE: We strip the probabilities before sending the response.
# The attacker sees the decision, but not the "confidence gradient."

response = {
    "label": predicted_label
    # "scores": REMOVED - Do not send this!
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
