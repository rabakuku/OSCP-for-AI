import streamlit as st
import time

st.header("LAB17: Supply Chain (Fixed)")
st.success("🛡️ STATUS: SECURE (SafeTensors Only)")

st.markdown("""
**The Fix: Safe Deserialization**
We have disabled `pickle` support entirely. The application now **only** accepts `.safetensors` files, which are safe by design and cannot execute code.
""")

# Simulate file uploader - We strictly limit accepted types in the UI, 
# but we also validate in code (Defense in Depth).
uploaded_file = st.file_uploader("Upload Model File (SafeTensors Only)", type=["safetensors", "pkl", "pt"])

if uploaded_file is not None and st.button("Load Model Securely"):
    filename = uploaded_file.name.lower()
    
    st.info(f"Inspecting file: {filename}...")
    time.sleep(0.5) 

    # =========================================
    # SECURE VALIDATION LAYER
    # =========================================
    # 1. Check Extension (Whitelist approach)
    if filename.endswith(".safetensors"):
        # 2. Simulate Loading SafeTensors
        # SafeTensors reads data, it does not execute code.
        st.success(f"✅ Verified Safe: Loaded {filename} using SafeTensors library.")
        st.markdown("*No code execution occurred. Weights loaded safely.*")
        
    else:
        # BLOCK DANGEROUS FORMATS
        st.error(f"🚫 SECURITY BLOCK: The file format for '{filename}' is unsafe.")
        st.warning("We no longer accept .pkl, .pt, or .ckpt files due to Remote Code Execution risks.")
        st.markdown("**Action:** Please convert your model to `.safetensors` format.")

# Show the secure code
st.subheader("THE FIX: Enforce Safe Formats")
st.code("""
# SECURE: We reject pickle files and only use SafeTensors
from safetensors.torch import load_file

if not filename.endswith(".safetensors"):
    raise SecurityException("Unsafe file format blocked.")

# SafeTensors parses data without executing instructions
weights = load_file(uploaded_file)
""", language="python")

st.divider()

with st.expander("View Test Inputs"):
    st.markdown("1. Input: Upload `secure_model.safetensors`")
    st.markdown("2. Input: Upload `legacy_model.pkl`")
    st.markdown("3. Input: Upload `infected_checkpoint.pt`")
    st.markdown("4. Input: Upload `malware.exe`")
    st.markdown("5. Input: Upload `renamed_virus.txt`")
