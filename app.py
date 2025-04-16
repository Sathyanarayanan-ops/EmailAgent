import streamlit as st
from orchestrator.master_graph import build_master_graph

# Build LangGraph master agent once
orchestrator = build_master_graph()

st.set_page_config(page_title="Enterprise Agent", page_icon="🤖")
st.title("🤖 Enterprise Master Agent")

# Sidebar
with st.sidebar:
    st.markdown("### What can I ask?")
    st.markdown("""
    - `"Show me the latest code commits"`
    - `"Summarize my email inbox"`
    - `"What are the employee leave requests?"`
    """)

# Chat input
user_input = st.text_input("Ask the master agent something:")

if st.button("Run") and user_input:
    with st.spinner("Running agent..."):
        state = {
            "user_input": user_input,
            "chat_history": []  # Can store session history here
        }
        result = orchestrator.invoke(state)
        outputs = result.get("agent_outputs", {})
        response_text = next(iter(outputs.values()), "No response.")

    st.markdown("### ✅ Agent Response")
    st.success(response_text)
