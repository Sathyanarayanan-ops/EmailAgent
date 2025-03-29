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
    param1: str
    param2: str
    


graph_builder = StateGraph(State)


