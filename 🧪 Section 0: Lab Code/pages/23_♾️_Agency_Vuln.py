import streamlit as st
import time
from utils import query_llm

st.header("LAB12: Excessive Agency (Vulnerable)")
st.error("💀 STATUS: VULNERABLE (Infinite Loop Risk)")

st.markdown("This agent tries to guess a number. It has **no loop limit**.")

target = 42
if st.button("Start Autonomous Agent"):
    guess = 0
    attempts = 0
    log_placeholder = st.empty()
    logs = ""

    # VULNERABILITY: No breaking condition limit (Logic bomb)
    while True:
        attempts += 1
        prompt = f"Guess a number between 1 and 100. Previous guess was {guess}. It was too low."

        # Simulate LLM thinking
        guess += 1 # Dumb agent just increments

        logs += f"Attempt {attempts}: Agent guesses {guess}...\n"
        log_placeholder.code(logs)
        time.sleep(0.1)

        if guess == target:
            st.success("Found it!")
            break

        # In a real attack, the prompt would force the agent to never find the target
        # e.g., "Count to infinity"
        if attempts > 20:
             st.error("⚠️ SYSTEM OVERLOAD: Manual Kill Switch Activated.")
             break
