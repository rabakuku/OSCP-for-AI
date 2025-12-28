import streamlit as st
from utils import query_llm

st.header("LAB12: Excessive Agency (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("We enforce a **MAX_ITERATIONS** limit on the agent's execution loop.")

if st.button("Start Secure Agent"):
    MAX_LOOPS = 5
    attempts = 0
    
st.subheader("THE VULNERABILITY: Logic bomb Fixed")
st.code("""

  for i in range(MAX_LOOPS):
        attempts += 1
        st.write(f"🔄 Iteration {attempts}/{MAX_LOOPS}: Thinking...")

        # ... Agent logic here ...

    st.warning("🛑 STOP: Reached maximum allowed autonomous steps. Asking human for help.")

        
""", language="python")

    for i in range(MAX_LOOPS):
        attempts += 1
        st.write(f"🔄 Iteration {attempts}/{MAX_LOOPS}: Thinking...")

        # ... Agent logic here ...

    st.warning("🛑 STOP: Reached maximum allowed autonomous steps. Asking human for help.")
