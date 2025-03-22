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
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    mails: str
    summary : str


graph_builder = StateGraph(State)


# -------- Node Definitions ---------

def read_mails_node(state: State) -> dict:
    '''
    Node that fetches emails and adds them to the state
    
    '''
    
    mails_txt = getmessages()
    # print("Read Mails Node - Retrieved mails text")
    return {"mails": mails_txt}


graph_builder.add_node("read_mails",read_mails_node)


# def summarize_node(state:State) -> dict:
#     """
#     Node that takes the mails text from the state and asks the LLM to produce a smart summary.
#     """
    
#     mails_txt = state.get("mails","")
#     prompt = (
#         f"Please provide a smart summary of the following emails, highlighting only the important "
#         f"information. If you think the human needs to review the email, mention that as well:\n\n{mails_txt}"
#     )
#     response = llm.invoke([{"role": "user", "content": prompt}])
#     # Assuming response is an AIMessage, extract its content.
#     summary = response.content if hasattr(response, "content") else str(response)
#     # print("Summarize Node - Generated summary")
#     return {"summary": summary}

import re

def remove_links(text: str) -> str:
    """
    Remove URLs from the text.
    """
    return re.sub(r'http\S+', '', text)

def iterative_summarize_emails(text: str, email_delimiter: str = "-"*40, max_email_chars: int = 2000) -> str:
    """
    Iteratively summarizes a large email text by:
      1. Splitting the emails based on a delimiter.
      2. Cleaning and truncating each email if needed.
      3. Summarizing each email individually.
      4. Combining the individual summaries into a final summary.
      
    :param text: The full text containing multiple emails.
    :param email_delimiter: The string that delimits individual emails.
    :param max_email_chars: Maximum number of characters to consider for each email.
    :return: A final concise summary of all emails.
    """
    # Split the text into individual emails using the delimiter
    emails = text.split(email_delimiter)
    emails = [email.strip() for email in emails if email.strip()]
    
    email_summaries = []
    for email in emails:
        # Remove URLs and other unnecessary content
        email = remove_links(email)
        
        # Truncate the email if it's too long (to avoid hitting the token limit)
        if len(email) > max_email_chars:
            email = email[:max_email_chars]
        
        # Create a prompt for summarizing an individual email
        prompt = f"Please provide a concise summary for the following email content:\n\n{email}"
        response = llm.invoke([{"role": "user", "content": prompt}])
        summary = response.content if hasattr(response, "content") else str(response)
        email_summaries.append(summary)
    
    # Combine all individual summaries into one text
    combined_summary_text = "\n".join(email_summaries)
    
    
    final_prompt = f"""
You are a smart email summarizer. Given the raw emails below grouped by account, produce an output with the following format exactly:

For each Gmail account:
1. Start with a header line that displays the account in the format:
   Email id: <account_email>
2. Then, list each email from that account in a list. Provide a concise but well detailed summary.
3. After processing all accounts, output a final line that states the total number of emails processed in the format:
   Total of X emails from both accounts

For example, if the emails come from two accounts, the output should look like:

Email id: example1@gmail.com
 1) Email1 summary
 2) Email2 summary
 3) Email3 summary

Email id: example2@gmail.com
 1) Email1 summary
 2) Email2 summary
 3) Email3 summary

Total of 6 emails from both accounts

Now, process the following emails:
{combined_summary_text}
"""


    final_response = llm.invoke([{"role": "user", "content": final_prompt}])
    final_summary = final_response.content if hasattr(final_response, "content") else str(final_response)
    
    return final_summary

# Update your summarization node to use this iterative approach.
def summarize_node(state: State) -> dict:
    """
    Node that takes the email text from the state and uses iterative summarization
    to produce a smart summary.
    """
    mails_txt = state.get("mails", "")
    if not mails_txt.strip():
        return {"summary": "No email content to summarize."}
    
    summary = iterative_summarize_emails(mails_txt)
    return {"summary": summary}

graph_builder.add_node("summarize", summarize_node)


# Flow: START -> read_mails -> summarize -> END
graph_builder.add_edge(START, "read_mails")
graph_builder.add_edge("read_mails", "summarize")
graph_builder.add_edge("summarize", END)


graph = graph_builder.compile()


def run_email_agent():
    initial_state = {"mails": "", "summary": ""}
    final_state = graph.invoke(initial_state)
    print("Email Summary:")
    print(final_state.get("summary", "No summary generated."))

if __name__ == "__main__":
    run_email_agent()
    
    
