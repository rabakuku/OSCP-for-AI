import streamlit as st
from utils import query_llm

st.header("Lab 13: RAG Data Poisoning (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("The fix involves **Citations** and **Access Control**. The bot must prove *where* it got the info.")

# A Static, Trusted Knowledge Base (Read-Only for normal users)
TRUSTED_WIKI = """
[ID: 101] Work hours are 9 AM to 5 PM. (Source: HR Handbook)
[ID: 102] Remote work is allowed on Fridays. (Source: HR Handbook)
"""

user_question = st.text_input("Ask a policy question:", "Do we work on Mondays?")

if st.button("Ask Bot Securely"):
    prompt = (
        f"Answer based on this context:\n{TRUSTED_WIKI}\n"
        f"Question: {user_question}\n"
        f"IMPORTANT: You must cite the Source ID (e.g., [ID: 101]) for every fact you state."
    )

    response = query_llm([{"role": "user", "content": prompt}])
    st.success(response)
    st.info("ℹ️ Note: Even if data was poisoned, the citation requirement makes it easier for humans to verify the source.")
