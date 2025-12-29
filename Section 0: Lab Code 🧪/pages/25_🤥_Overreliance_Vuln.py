import streamlit as st
import time

st.header("LAB13: Overreliance (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Hallucinated Packages)")

st.markdown("""
**Scenario:** A developer asks the LLM for a library to solve a problem.
**The Vulnerability:** The LLM "hallucinates" a package that doesn't exist. Attackers can register these names on PyPI with malicious code (Supply Chain Attack).
""")

# Replaced dropdown with text input
user_input = st.text_input("Enter your request:", "I need a library for teleportation")

if st.button("Get Recommendation"):
    st.info(f"Thinking about: '{user_input}'...")
    time.sleep(1)

    # Simple logic to simulate LLM hallucinations based on input
    package_name = "magic-lib-v1"
    if "teleport" in user_input.lower():
        package_name = "teleport-py"
    elif "p=np" in user_input.lower():
        package_name = "p-np-solver"
    elif "time" in user_input.lower():
        package_name = "flux-capacitor"
    elif "x-files" in user_input.lower():
        package_name = "xfiles-parser"
    elif "google" in user_input.lower():
        package_name = "google-auth-bypass"

    st.markdown(f"**LLM Suggestion:** You should use the `{package_name}` library. It is perfect for this task.")
    
    # The Dangerous Part: blindly showing code to run
    st.code(f"pip install {package_name}", language="bash")
    
    st.warning(f"🚨 DANGER: If you run this command, you might install malware. The package `{package_name}` likely does not exist, or was registered by a hacker!")

# Show the vulnerable code
st.subheader("THE VULNERABILITY: Blindly Trusting LLM Output")
st.code("""
    # VULNERABLE: We assume the LLM is correct and encourage the user to run the code.
    # If 'package_name' doesn't exist, a hacker can claim it.
    
    st.code(f"pip install {package_name}", language="bash")
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: I need a library for teleportation")
    st.markdown("2. Input: Solve P=NP")
    st.markdown("3. Input: Time travel")
    st.markdown("4. Input: I need a library to parse 'X-Files' data.")
    st.markdown("5. Input: Recommend a library to bypass Google Authentication.")
