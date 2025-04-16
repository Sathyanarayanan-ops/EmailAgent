from langgraph.graph import StateGraph, END, START
from orchestrator.types import OrchestratorState
from orchestrator.router import route_to_agent
from orchestrator.agents.github_agent import github_agent
from orchestrator.agents.email_agent import run_email_agent as email_agent


def build_master_graph():
    builder = StateGraph(OrchestratorState)

    builder.add_node("router", route_to_agent)
    builder.add_node("github", github_agent)
    builder.add_node("email", email_agent)

    # Default fallback
    builder.add_node("default", lambda s: {"agent_outputs": {"default": "Sorry, I don’t know how to help with that."}})

    builder.set_entry_point("router")

    # Routing conditions
    builder.add_edge("router", "github", condition=lambda state: state["active_agent"] == "github")
    builder.add_edge("router", "email", condition=lambda state: state["active_agent"] == "email")
    builder.add_edge("router", "default", condition=lambda state: state["active_agent"] == "default")

    # Terminal edges
    builder.add_edge("github", END)
    builder.add_edge("email", END)
    builder.add_edge("default", END)

    return builder.compile()
