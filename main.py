from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


from orchestrator.master_graph import build_master_graph

orchestrator = build_master_graph()

def run_master_agent(user_input: str):
    state = {
        "user_input": user_input,
        "chat_history": []
    }

    result = orchestrator.invoke(state)
    print(result["agent_outputs"])

if __name__ == "__main__":
    run_master_agent("Give me the last 2 commits from the repo")
