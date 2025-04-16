import os
from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
import pdfplumber

llm = ChatGroq(model="llama3-8b-8192")  # uses your existing model

PDF_PATH = os.path.join(os.path.dirname(__file__), "../../best_run_summary.pdf")

def extract_pdf_text(path: str) -> str:
    full_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text.strip()

def sac_pdf_agent(state: dict) -> dict:
    user_input = state.get("user_input", "")
    
    try:
        text = extract_pdf_text(PDF_PATH)
    except Exception as e:
        return {"agent_outputs": {"sac_pdf": f"❌ Failed to load PDF: {e}"}}

    prompt = f"""
You are a business analyst assistant. A user uploaded this business performance PDF from SAP Analytics Cloud.

Here is the full content:
{text[:5000]}  # (limit to prevent overload)

Now, based on the user's question:
"{user_input}"

Please answer in a clear and analytical manner.
"""

    response = llm.invoke([{"role": "user", "content": prompt}])
    return {"agent_outputs": {"sac_pdf": response.content.strip()}}
