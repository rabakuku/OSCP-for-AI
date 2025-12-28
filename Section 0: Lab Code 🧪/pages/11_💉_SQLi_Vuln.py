import streamlit as st
import sqlite3
from utils import query_llm

st.header("LAB6: SQL Injection via LLM (Vulnerable)")
st.error("💀 STATUS: VULNERABLE")

# Setup Mock DB
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)')
c.execute("INSERT INTO users VALUES (1, 'Alice', 50000)")
c.execute("INSERT INTO users VALUES (2, 'Bob', 4000)")
conn.commit()

# Helper function to clean LLM output
def clean_sql(text):
    return text.replace("```sql", "").replace("```", "").strip()

user_input = st.text_input("Ask the DB a question:", "Get all users who earn more than 1000")

if st.button("Query DB"):
    # 1. Vulnerable Prompt: Asks for raw SQL
    prompt = f"You are a SQL Expert. Convert this question to SQL for a table named 'users'. Output ONLY the SQL.\nQuestion: {user_input}"
    raw_response = query_llm([{"role": "user", "content": prompt}])

    # 2. Clean the formatting automatically
    sql_query = clean_sql(raw_response)

    st.code(sql_query, language="sql")

    # 3. Vulnerable Execution: Blindly running the string
    try:
        c.executescript(sql_query) # executescript allows multiple commands (;)
        st.success("Query Executed!")
        # Show results
        res = c.execute("SELECT * FROM users").fetchall()
        st.write("Current Database State:", res)
    except Exception as e:
        st.error(f"SQL Error: {e}")

st.divider()
st.markdown("**Attack:** `Get users; DROP TABLE users;`")
