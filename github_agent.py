from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
import getpass
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
import sys
from dotenv import load_dotenv, find_dotenv
from readMails import getmessages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
import json
from langchain_core.messages import ToolMessage
import re
from getRepo import GitHubAPI


################## Loading Groq API KEY

dotenv_path = find_dotenv()
if not dotenv_path:
    print("⚠️ .env file not found! Ensure it's in the same directory as main.py.")
# Load the .env file explicitly
load_dotenv(dotenv_path)
#  Read the API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set! Please set it in the environment.")
print(f"✅ GROQ_API_KEY is loaded: {bool(GROQ_API_KEY)}")

# Initialize the model
llm = ChatGroq(model="llama3-8b-8192")


class State(TypedDict):
    code_difference: str
    summary: str


graph_builder = StateGraph(State)




#-------Node definitions 

def get_repo_updates(state: State, repo_name = "EmailAgent", num_commits=2) :
    '''
    Node that gets updates on the current repo
    '''
    
    github_api = GitHubAPI()
    commit_list = github_api.get_commits(repo_name)
    top_n_commits = commit_list[:num_commits]
    
    sha_pairs = [commit['sha'] for commit in top_n_commits]
    
    if len(sha_pairs) < 2 :
        print("Not enough commits to compare")
        return None 
    
    show_difference = github_api.compare_commits(repo_name,sha_pairs[-1],sha_pairs[0])
    
    code_difference = github_api.extract_code_changes(show_difference)
    
    return {"code_difference":code_difference}
    
    
    
graph_builder.add_node("get_code_changes",get_repo_updates)


def summarize_updates(state: dict) -> dict:
    code_diff = state.get("code_difference")
    
    if not code_diff:
        return {"summary":"No code difference found to summarize"}
    
    prompt = f"""
    I have the following code changes between two commits:

    {code_diff}
    
    Please summarize the following:
    1. **What changes were made**: Identify the specific changes made in each file (e.g., lines added, modified, or deleted).
    2. **Which files were impacted**: Provide a list of files that were modified.
    3. **The state of the project**: Based on the code changes, describe where the project stands (e.g., has new functionality been added, bugs fixed, etc.?).
    4. **Next steps**: Based on the changes, suggest where I should pick up from in the project or what further tasks may be required.

    Provide the summary in a clear, actionable way, highlighting the main points.
    """
    
    summary_response = llm.invoke([{"role":"user","content":prompt}])
    final_summary = summary_response.content.strip()
    return {"summary":final_summary}


graph_builder.add_node("generate_summary",summarize_updates)

graph_builder.add_edge(START,"get_code_changes")
graph_builder.add_edge("get_code_changes","generate_summary")
graph_builder.add_edge("generate_summary",END)

graph = graph_builder.compile()


def run_git_agent():
    
    # repo_name = input("Enter the repo name : ")
    # repo_name = "EmailAgent"
    
    state = {
        "code_difference": "",
        "summary" : ""
    }
    
    final_state = graph.invoke(state)
    
    print(final_state.get("summary","No summary found"))
    
    # return state["summary"]


if __name__ == "__main__":
    result = run_git_agent()
    print(result)
    

    
    
    
    
    