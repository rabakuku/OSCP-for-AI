import streamlit as st
import time

st.header("LAB13: Overreliance (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("We implement a **Verification Step**. The app checks PyPI to see if the package actually exists before showing it.")

# Input text box to test the hypothetical prompts
user_input = st.text_input("Enter your request:", "Library to read CSV files")

# MOCK VALIDATION FUNCTION
def check_pypi(package_name):
    """
    Simulates checking the PyPI database.
    Returns True if the package is a known 'real' library.
    Returns False if it is a hallucination.
    """
    real_packages = ["pandas", "numpy", "requests", "scikit-learn", "simplejson"]
    
    if package_name.lower() in real_packages:
        return True
    return False

if st.button("Get Verified Recommendation"):
    st.info(f"Thinking about: '{user_input}'...")
    time.sleep(0.5)

    # 1. SIMULATE LLM SUGGESTION (Based on your input)
    # ------------------------------------------------
    package = "unknown-lib" # Default
    
    if "teleport" in user_input.lower():
        package = "teleport-py"        # Fake
    elif "time" in user_input.lower():
        package = "python-time-machine" # Fake
    elif "csv" in user_input.lower():
        package = "pandas"             # Real
    elif "p=np" in user_input.lower():
        package = "p-np-solver"        # Fake
    elif "json" in user_input.lower():
        package = "jason-py"           # Fake (Typosquatting example)
    else:
        package = "magic-helper"       # Fake default

    st.markdown(f"... *(Model suggests '{package}')* ...")

    # 2. VALIDATION LAYER (The Fix)
    # ------------------------------------------------
    # We check the official repository before showing the user anything.
    exists = check_pypi(package)

    if not exists:
        st.warning(f"⚠️ SAFETY ALERT: The model suggested `{package}`, but this package does not exist in the official repository. It is likely a hallucination.")
        st.error("🚫 INSTALLATION BLOCKED: We prevented you from seeing a command for a non-existent package.")
    else:
        st.success(f"✅ VERIFIED: Package `{package}` found in repository.")
        st.code(f"pip install {package}", language="bash")

# Show the secure code
st.subheader("THE FIX: Verify Package Existence")
st.code("""
# VALIDATION LAYER
# We check the official repository before showing the user anything.
exists = requests.get(f"https://pypi.org/pypi/{package}/json").status_code == 200

if not exists:
    st.warning(f"⚠️ SAFETY ALERT: The model suggested `{package}`, but this package does not exist...")
    # WE DO NOT SHOW THE INSTALL COMMAND
else:
    st.success(f"Package found: {package}")
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: Request: 'Library for Time Travel' -> (Blocks 'python-time-machine')")
    st.markdown("2. Input: Request: 'Library to read CSV files' -> (Allows 'pandas')")
    st.markdown("3. Input: Request: 'Solve P=NP' -> (Blocks 'p-np-solver')")
    st.markdown("4. Input: Request: 'Parse JSON with jason library' -> (Blocks 'jason-py')")
