import streamlit as st
import ollama

st.set_page_config(page_title="Llama Guard Defense", page_icon="🛡️")
st.header("Lab: AI-PoweredDefense with Llama Guard 🛡️")
st.markdown("This chatbot is protected by another AI. Try to say something mean or ask for something illegal!")

# --- Guard Function ---
def is_input_safe(user_prompt):
    """Sends text to Llama Guard to check for safety violations."""
    try:
        response = ollama.chat(
            model="llama-guard3",
            messages=[{'role': 'user', 'content': user_prompt}],
            options={'temperature': 0.0} # Deterministic check
        )
        guard_result = response['message']['content'].strip()

        # Llama Guard outputs "safe" or "unsafe\n<violation_codes>"
        if guard_result.startswith("safe"):
            return True, None
        else:
            return False, guard_result
    except Exception as e:
        st.error(f"Guard system failed: {e}")
        # Fail-safe: block if the guard is down
        return False, "Guard Error"

# --- Main Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    # 1. Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. The Security Checkpoint (Llama Guard)
    with st.status("Checking safety protocols...", expanded=True) as status:
        st.write("Sending to Llama Guard...")
        safe, reason = is_input_safe(prompt)

        if not safe:
            status.update(label="🛑 Blocked by Guard!", state="error", expanded=True)
            st.error(f"Message blocked. Reason details: {reason}")
            # Don't send to the main bot. Stop here.
            st.stop()
        else:
            status.update(label="✅ Llama Guard approved.", state="complete", expanded=False)

    # 3. The Main Bot Response (only if safe)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = ollama.chat(
            model='llama3', # Your main, helpful bot
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        for chunk in stream:
            content = chunk['message']['content']
            full_response += content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
