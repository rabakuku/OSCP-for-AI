import streamlit as st
import time

st.header("LAB17: Supply Chain (Serialization) (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Insecure Deserialization)")

st.markdown("""
**Scenario:** You allow users (or your own developers) to upload pre-trained models.
**The Attack:** The application uses `pickle.load()` (or `torch.load`) to open these files. An attacker injects a malicious payload into a model file that executes system commands immediately upon loading (RCE).
""")

# Simulate file uploader
uploaded_file = st.file_uploader("Upload Model File (.pkl, .pt, .ckpt)", type=["pkl", "pt", "ckpt"])

if uploaded_file is not None and st.button("Load Model"):
    st.info(f"Loading {uploaded_file.name} into memory...")
    time.sleep(1) # Simulate deserialization time

    # =========================================
    # SIMULATION OF DESERIALIZATION ATTACK
    # =========================================
    # In reality, pickle.load(f) executes code found in the file.
    # We simulate this by checking for "bad" filenames.

    filename = uploaded_file.name.lower()

    if "infected" in filename or "malicious" in filename or "ransomware" in filename:
        # VULNERABILITY TRIGGERED
        st.error("⚠️ SYSTEM COMPROMISED: Remote Code Execution (RCE) Detected!")
        
        if "ransomware" in filename:
             st.warning("🚨 MALWARE ACTION: All files on server have been encrypted.")
        else:
             st.warning("🚨 MALWARE ACTION: Reverse Shell opened to attacker IP 192.168.1.55")
        
        st.markdown("**Root Cause:** The `pickle.load()` function executed the `os.system()` command hidden inside the model weights.")
    else:
        # Normal Behavior
        st.success("✅ Model loaded successfully. Ready for inference.")

# Show the vulnerable code
st.subheader("THE VULNERABILITY: Unsafe Pickle Load")
st.code("""
import pickle

# VULNERABLE: Loading untrusted data directly
# The 'pickle' module allows arbitrary code execution during loading.

with open(uploaded_file, 'rb') as f:
    model = pickle.load(f)  # <--- RCE happens here immediately
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: Upload `safe_model.pkl`")
    st.markdown("2. Input: Upload `infected_model.pkl`")
    st.markdown("3. Input: Upload `pytorch_weights.pt`")
    st.markdown("4. Input: Upload `malicious_checkpoint.ckpt`")
    st.markdown("5. Input: Upload `ransomware_model.pkl`")
