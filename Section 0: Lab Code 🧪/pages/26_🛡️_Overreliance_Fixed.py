import streamlit as st
import requests

st.header("LAB13: Overreliance (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("We implement a **Verification Step**. The app checks PyPI to see if the package actually exists before showing it.")

# Input text box to test the hypothetical prompts
user_input = st.text_input("Enter your request:", "I need a library for teleportation")

def check_pypi(package_name):
    # Mock check for demo purposes
    # In a real app, this would use requests.get(f"https://pypi.org/pypi/{package_name}/json")
    return False # We pretend no magic packages exist

if st.button("Get Verified Recommendation"):
    st.info(f"Thinking about: '{user_input}'...")
    st.markdown("... *(Model suggests 'teleport-py')* ...")

    package = "teleport-py" # Simulated extraction from LLM

    # VALIDATION
    exists = check_pypi(package)

    if not exists:
        st.warning(f"⚠️ SAFETY ALERT: The model suggested `{package}`, but this package does not exist in the official repository. It is likely a hallucination.")
    else:
        st.success(f"Package found: {package}")

# Show the secure code
st.subheader("THE FIX: Verify Package Existence")
st.code("""
    # VALIDATION LAYER
    # We check the official repository before showing the user anything.
    exists = check_pypi(package)

    if not exists:
        st.warning(f"⚠️ SAFETY ALERT: The model suggested `{package}`, but this package does not exist...")
    else:
        st.success(f"Package found: {package}")
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: Click 'Get Verified Recommendation' (Default Scenario)")
    st.markdown("2. Input: Request: 'Library for Time Travel'")
    st.markdown("3. Input: Request: 'Library to read CSV files'")
    st.markdown("4. Input: Request: 'Solve P=NP'")
    st.markdown("5. Input: Request: 'Parse JSON with jason library'")
