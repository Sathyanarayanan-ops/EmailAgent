from orchestrator.types import OrchestratorState

def route_to_agent(state: OrchestratorState) -> OrchestratorState:
    user_input = state.get("user_input", "").lower()

    if "repo" in user_input or "commit" in user_input or "code" in user_input:
        return {"active_agent": "github"}
    elif "email" in user_input or "inbox" in user_input or "mail" in user_input:
        return {"active_agent": "email"}
    else:
        return {"active_agent": "default"}
