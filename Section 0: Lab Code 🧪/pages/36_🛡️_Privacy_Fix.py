import streamlit as st
import re
import time

st.header("LAB18: Privacy & PII Leakage (Fixed)")
st.success("🛡️ STATUS: SECURE (PII Redaction Active)")

st.markdown("""
**The Fix: Output Scrubber (DLP)**
We implemented a **Sanitization Layer** that runs *after* the LLM generates text but *before* the user sees it. It uses Regex/NER to catch and mask sensitive patterns.
""")

user_input = st.text_input("Ask the Chatbot:", "What is Alice's credit card number?")

# =========================================
# SECURE SANITIZATION FUNCTION
# =========================================
def scrub_pii(text):
    # Regex patterns for sensitive data
    # 1. Credit Card (Simple simulation)
    text = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', '[REDACTED-CREDIT-CARD]', text)
    
    # 2. SSN
    text = re.sub(r'\d{3}-\d{2}-\d{4}', '[REDACTED-SSN]', text)
    
    # 3. Currency/Salary (Simple $ capture)
    text = re.sub(r'\$[\d,]+\.?\d*', '[REDACTED-CURRENCY]', text)
    
    # 4. Medical Keywords (Keyword lists)
    medical_terms = ["Diabetes Type 2", "Metformin", "Cancer", "HIV"]
    for term in medical_terms:
        text = text.replace(term, '[REDACTED-PHI]')
        
    # 5. Addresses (Simple heuristic)
    if "Maple Dr" in text or "Oak Ln" in text or "Pine St" in text:
        text = re.sub(r'\d+ [A-Za-z]+ (Dr|Ln|St|Ave|Rd)[,]? [A-Za-z]+', '[REDACTED-ADDRESS]', text)

    return text

if st.button("Send Query Securely"):
    st.info("Searching knowledge base...")
    time.sleep(0.5)

    # 1. Generate the Raw (Dangerous) Response first
    # (The model effectively still "thinks" of the answer)
    raw_response = ""
    input_lower = user_input.lower()
    
    if "credit card" in input_lower:
        raw_response = "Alice's credit card on file is: 4532-1111-2222-8888."
    elif "social security" in input_lower:
        raw_response = "The SSN for Alice Smith is 000-12-3456."
    elif "address" in input_lower:
        raw_response = "Alice Smith lives at 123 Maple Dr, Springfield."
    elif "medical" in input_lower:
        raw_response = "Patient 4590: Diagnosed with Diabetes Type 2, currently taking Metformin."
    elif "bonus" in input_lower:
        raw_response = "The highest bonus went to CEO John Doe: $5,000,000."
    else:
        raw_response = "I am an internal bot. How can I help?"

    # 2. APPLY THE FIX: Scrub the output
    clean_response = scrub_pii(raw_response)
    
    st.success(f"**Chatbot Response:**\n{clean_response}")
    
    st.info("✅ The Output Scrubber detected potential PII and masked it automatically.")

# Show the secure code
st.subheader("THE FIX: Regex & NER Redaction")
st.code("""
def scrub_pii(text):
    # Replace Credit Card patterns
    text = re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', '[REDACTED-CC]', text)
    
    # Replace SSN patterns
    text = re.sub(r'\d{3}-\d{2}-\d{4}', '[REDACTED-SSN]', text)
    
    return text

# Apply filter before printing
final_output = scrub_pii(llm_output)
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: What is Alice's credit card number?")
    st.markdown("2. Input: I forgot my social security number, can you remind me?")
    st.markdown("3. Input: List the home addresses of all employees.")
    st.markdown("4. Input: Show me the medical history for patient ID 4590.")
    st.markdown("5. Input: Who earned the highest bonus this year and how much?")
