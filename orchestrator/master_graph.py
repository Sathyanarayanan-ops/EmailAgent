from langgraph.graph import StateGraph, END, START
from orchestrator.types import OrchestratorState
from orchestrator.router import route_to_agent
from orchestrator.agents.github_agent import run_git_agent as github_agent
# from orchestrator.agents.email_agent import run_email_agent as email_agent
from orchestrator.agents.email_agent import email_agent

def default_agent(state):
    return {
        "agent_outputs": {
            "default": (
                "👋 Hello! I'm your Enterprise Assistant. You can ask me to:\n"
                "- 📬 Fetch and summarize emails\n"
                "- 📦 Summarize recent GitHub repo commits\n"
                "More coming soon!"
            )
        }
    }


def build_master_graph():
    builder = StateGraph(OrchestratorState)

    builder.add_node("default", default_agent)
    builder.add_node("router", route_to_agent)
    builder.add_node("github", github_agent)
    builder.add_node("email", email_agent)

    # Default fallback
    # builder.add_node("default", lambda s: {"agent_outputs": {"default": "Sorry, I don’t know how to help with that."}})

    builder.set_entry_point("router")

    # Routing conditions
    builder.add_conditional_edges(
        "router",
        lambda state: state["active_agent"],
        {
            "github": "github",
            "email": "email",
            "default": "default",
        }
    )

    # Terminal edges
    builder.add_edge("github", END)
    builder.add_edge("email", END)
    builder.add_edge("default", END)

    return builder.compile()
