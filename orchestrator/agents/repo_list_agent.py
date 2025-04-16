from orchestrator.agents.getRepo import GitHubAPI

def repo_list_agent(state):
    github = GitHubAPI()
    repos = github.get_repo_list()
    return {
        "agent_outputs": {
            "repo_list": "Here are your repositories:\n- " + "\n- ".join(repos)
        }
    }
