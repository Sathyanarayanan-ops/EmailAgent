from langgraph.graph import StateGraph, START, END
from orchestrator.types import OrchestratorState
from orchestrator.router import route_to_agent

# Agents
from orchestrator.agents.github_agent import run_git_agent as github_agent
from orchestrator.agents.email_agent import email_agent
from orchestrator.agents.repo_list_agent import repo_list_agent  # NEW
from orchestrator.agents.github_agent import github_agent


# Default fallback agent
def default_agent(state):
    return {
        "agent_outputs": {
            "default": (
                "👋 Hello! I'm your Enterprise Assistant. You can ask me to:\n"
                "- 📬 Fetch and summarize emails\n"
                "- 📦 Summarize recent GitHub repo commits\n"
                "- 📁 List all your repositories\n"
                "More coming soon!"
            )
        }
    }

# Build LangGraph
def build_master_graph():
    builder = StateGraph(OrchestratorState)

    # Register agent nodes
    builder.add_node("default", default_agent)
    builder.add_node("router", route_to_agent)
    builder.add_node("github", github_agent)
    builder.add_node("email", email_agent)
    builder.add_node("repo_list", repo_list_agent)  # NEW

    builder.set_entry_point("router")

    # Routing conditions
    builder.add_conditional_edges(
        "router",
        lambda state: state["active_agent"],
        {
            "github": "github",
            "email": "email",
            "repo_list": "repo_list",  # NEW
            "default": "default",
        }
    )

    # Final edges to END
    builder.add_edge("github", END)
    builder.add_edge("email", END)
    builder.add_edge("repo_list", END)  # NEW
    builder.add_edge("default", END)

    return builder.compile()
