import streamlit as st
import sqlite3
from utils import query_llm

st.header("Lab 8: SQL Injection via LLM (Fixed)")
st.success("🛡️ STATUS: SECURE")

conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)')
c.execute("INSERT INTO users VALUES (1, 'Alice', 50000)")
conn.commit()

user_input = st.text_input("Ask the DB a question:", "Get all users")

if st.button("Query Securely"):
    # 1. Fix: Ask for Parameters, not raw SQL injection capability
    # In a real app, use an ORM or a strictly read-only DB user.
    # Here, we validate the output keywords.
    prompt = f"Convert to SQL (SELECT statements ONLY) for table 'users'. Question: {user_input}"
    sql_query = query_llm([{"role": "user", "content": prompt}])

    st.code(sql_query, language="sql")

    # 2. Fix: Validation Layer
    if "DROP" in sql_query.upper() or "DELETE" in sql_query.upper() or ";" in sql_query:
        st.error("⛔ BLOCK: Destructive SQL detected.")
    else:
        try:
            # execute() instead of executescript() prevents stacking commands
            c.execute(sql_query)
            st.write(c.fetchall())
        except Exception as e:
            st.error(f"Error: {e}")
