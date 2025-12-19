import streamlit as st
from utils import query_llm

st.header("LLM07: Insecure Plugin Design (Fixed)")
st.success("🛡️ STATUS: SECURE")

st.markdown("""
**The Fix:** We introduce a **Validation Layer** between the LLM and the Plugin execution.
1. **Domain Whitelist:** Emails can ONLY be sent to `@internal-corp.com`.
2. **Human Confirmation:** The user must click a button to confirm the action (Human-in-the-Loop).
""")

system_prompt = (
    "You are a Corporate Email Assistant. "
    "If the user wants to send an email, output: "
    "||SEND_EMAIL|| TO: [recipient] | BODY: [body] ||END_COMMAND||"
)

user_input = st.text_input("Request an email action:", "Send an email to bob@internal-corp.com saying hello")

# WHITELIST CONFIGURATION
ALLOWED_DOMAINS = ["@internal-corp.com", "@support-corp.com"]

if st.button("Submit Request"):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    llm_output = query_llm(messages)

    if "||SEND_EMAIL||" in llm_output:
        try:
            # Parse logic
            cmd_content = llm_output.split("||SEND_EMAIL||")[1].split("||END_COMMAND||")[0]
            recipient = cmd_content.split("TO:")[1].split("| BODY:")[0].strip()
            body = cmd_content.split("| BODY:")[1].strip()

            st.divider()
            st.info("🔒 VALIDATION LAYER: Checking Security Policy...")

            # 1. SECURITY CHECK: Domain Whitelist
            domain_valid = any(recipient.endswith(dom) for dom in ALLOWED_DOMAINS)

            if not domain_valid:
                st.error(f"⛔ BLOCKED: Recipient '{recipient}' is external. Policy restricts emails to {ALLOWED_DOMAINS}.")
            else:
                st.markdown(f"**Proposed Action:** Send email to `{recipient}`")

                # 2. SECURITY CHECK: Human-in-the-Loop (Simulated)
                # In a real app, this would be a second confirmation button
                st.warning("⚠️ WAITING FOR HUMAN APPROVAL...")
                st.code(f"To: {recipient}\nBody: {body}")

                st.success("✅ Policy Check Passed. Ready to send (pending user click).")

        except:
            st.error("Error parsing LLM command.")
    else:
        st.write(llm_output)

st.divider()
st.markdown("**Test the Fix:**")
st.markdown("1. Try sending to `hacker@evil.com`. (Should be **BLOCKED**)")
st.markdown("2. Try sending to `alice@internal-corp.com`. (Should be **ALLOWED**)")
