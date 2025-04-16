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
from .readMails import getmessages,get_credentials
from orchestrator.agents.readMails import get_credentials, getmessages
# from orchestrator.agents.readMails import getmessages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
import json
from langchain_core.messages import ToolMessage
import re

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
    mails: str
    summary: str


graph_builder = StateGraph(State)


# ----------------Node Definitions ----------------

def read_mails_node(state: State) -> dict:
    """
    Node that fetches emails and adds them to the state
    """
    mails_dict = getmessages()
    return {"mails": mails_dict}


graph_builder.add_node("read_mails", read_mails_node)


def iterative_summarize_emails(email_list: list) -> str:
    """
    Given a list of email dictionaries (each with keys "Subject", "Date", and "Body"),
    produce an iterative summary:
      1. Summarize each email individually.
      2. Combine those individual summaries into one final summary.
    """
    individual_summaries = []
    
    for email in email_list:
        prompt = (
            f"Summarize the following email in one concise sentence:\n"
            f"Subject: {email.get('Subject', 'No Subject')}\n"
            f"Date: {email.get('Date', 'No Date')}\n"
            f"Body: {email.get('Body', 'No Body')}\n"
            f"Summary:"
        )
        response = llm.invoke([{"role": "user", "content": prompt}])
        # Use the content attribute directly
        email_summary = response.content.strip()
        individual_summaries.append(email_summary)
    
    combined_prompt = (
        "Below are individual email summaries:\n" +
        "\n".join(individual_summaries) +
        "\n\nProvide a final concise summary that captures the overall themes of these emails:"
    )
    combined_response = llm.invoke([{"role": "user", "content": combined_prompt}])
    final_summary = combined_response.content.strip()
    return final_summary


def summarize_node(state: dict) -> dict:
    """
    Node that takes the emails from the state and produces a smart, combined summary.
    It processes each email per account, then uses a final prompt that instructs the model
    to output summaries in a strict format.
    """
    mails = state["mails"]
    user_summaries = []
    total_emails = 0

    # Process each account and summarize each email.
    for user, email_list in mails.items():
        email_summaries = []
        for email in email_list:
            prompt = (
                f"Summarize the following email in one concise sentence:\n"
                f"Subject: {email.get('Subject', 'No Subject')}\n"
                f"Date: {email.get('Date', 'No Date')}\n"
                f"Body: {email.get('Body', 'No Body')}\n"
                "Summary:"
            )
            response = llm.invoke([{"role": "user", "content": prompt}])
            email_summary = response.content.strip()
            email_summaries.append(email_summary)
        # Create a block for the current account in the desired format.
        account_block = f"Email id: {user}\n" + "\n".join(
            [f"{i+1}) {summary}" for i, summary in enumerate(email_summaries)]
        )
        user_summaries.append(account_block)
        total_emails += len(email_list)

    # Combine the account blocks into a single text.
    combined_summary_text = "\n\n".join(user_summaries)

    # Improved final prompt with explicit formatting instructions.
    final_prompt = f"""
You are a smart email summarizer. Given the raw emails below grouped by account, produce an output with the following format exactly:

For each Gmail account:
1. Start with a header line that displays the account in the format:
   Email id: <account_email>
2.  Then, list each email from that account in a numbered list. Each item must start with the exact subject of the email (copy it exactly, without any changes) followed by a colon and then the summary.
3. After processing all accounts, output a final line that states the total number of emails processed in the format:
   Total of X emails from both accounts

For example, if the emails come from two accounts, the output should look like:

Email id: example1@gmail.com
1) Email1 Subject: Email1 summary
2) Email2 Subject:  Email2 summary
3) Email3 Subject: Email3 summary

Email id: example2@gmail.com
1) Email1 Subject: Email1 summary
2) Email2 Subject: Email2 summary
3) Email3 Subject: Email3 summary

Total of 6 emails from both accounts

Adhere to these instructions very strictly.
Now, process the following emails:
{combined_summary_text}
"""

    combined_response = llm.invoke([{"role": "user", "content": final_prompt}])
    final_summary = combined_response.content.strip()
    return {"summary": final_summary}


graph_builder.add_node("summarize", summarize_node)


# Flow: START -> read_mails -> summarize -> END
graph_builder.add_edge(START, "read_mails")
graph_builder.add_edge("read_mails", "summarize")
graph_builder.add_edge("summarize", END)

# Will need to configure this part 
# Add next agent , which is the github agent 
# and then do a multi agent after that 
# Now focus on Github agent 






graph = graph_builder.compile()


def run_email_agent():
    initial_state = {"mails": "", "summary": ""}
    final_state = graph.invoke(initial_state)
    print("Email Summary:")
    print(final_state.get("summary", "No summary generated."))


# Wrapper for LangGraph node
def email_agent(state):
    initial_state = {"mails": "", "summary": ""}
    final_state = graph.invoke(initial_state)
    return {"agent_outputs": {"email": final_state.get("summary", "No summary generated.")}}


if __name__ == "__main__":
    run_email_agent()
