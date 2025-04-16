import streamlit as st
from orchestrator.master_graph import build_master_graph

# Initialize the orchestrator once
orchestrator = build_master_graph()

st.set_page_config(page_title="Enterprise Master Agent", page_icon="🤖")

st.title("🧠 Enterprise Master Agent (LangGraph)")

# Sidebar
with st.sidebar:
    st.markdown("### Instructions")
    st.markdown("""
    - Ask questions like:
      - `"What changed in the repo?"`
      - `"Check my emails"`
      - `"Who applied for leave?"`
    - The agent will route your request and return the result.
    """)

# User input
user_input = st.text_input("Ask your enterprise assistant:")

if st.button("Send") and user_input:
    state = {
        "user_input": user_input,
        "chat_history": []  # Can persist this later
    }

    with st.spinner("Thinking..."):
        result = orchestrator.invoke(state)
        response = result.get("agent_outputs", {}).get(state.get("active_agent", "default"))

    if response:
        st.markdown("### 🤖 Agent Response")
        st.success(response)
    else:
        st.warning("No response from agent.")
