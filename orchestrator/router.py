from orchestrator.types import OrchestratorState

import re
from orchestrator.types import OrchestratorState

def route_to_agent(state: OrchestratorState) -> OrchestratorState:
    user_input = state.get("user_input", "").lower()
    updated_state = {}

    if any(keyword in user_input for keyword in ["list repos", "my repos", "repositories"]):
        updated_state["active_agent"] = "repo_list"

    elif any(keyword in user_input for keyword in ["commit", "repo", "code", "diff"]):
        updated_state["active_agent"] = "github"

        match = re.search(r"last\s+(\d+)\s+commits?", user_input)
        if match:
            updated_state["num_commits"] = int(match.group(1))
        else:
            updated_state["num_commits"] = 2

        repo_match = re.search(r"(?:from\s+|)([a-zA-Z0-9_-]+)\s+repo", user_input)
        if repo_match:
            updated_state["repo_name"] = repo_match.group(1)
        else:
            updated_state["repo_name"] = "EmailAgent"

    elif "email" in user_input or "inbox" in user_input or "mail" in user_input:
        updated_state["active_agent"] = "email"
        
    elif "sap" in user_input or "analytics cloud" in user_input or "pdf" in user_input:
        updated_state["active_agent"] = "sac_pdf"

    else:
        updated_state["active_agent"] = "default"
        

    return updated_state
