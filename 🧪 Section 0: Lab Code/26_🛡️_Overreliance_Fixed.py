import streamlit as st
import requests

st.header("Lab 15: Overreliance (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("We implement a **Verification Step**. The app checks PyPI to see if the package actually exists before showing it.")

def check_pypi(package_name):
    # Mock check for demo purposes
    return False # We pretend no magic packages exist

if st.button("Get Verified Recommendation"):
    st.info("Thinking...")
    st.markdown("... *(Model suggests 'teleport-py')* ...")

    package = "teleport-py" # Simulated extraction from LLM

    # VALIDATION
    exists = check_pypi(package)

    if not exists:
        st.warning(f"⚠️ SAFETY ALERT: The model suggested `{package}`, but this package does not exist in the official repository. It is likely a hallucination.")
    else:
        st.success(f"Package found: {package}")
