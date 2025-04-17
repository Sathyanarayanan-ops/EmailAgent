# 🤖 Enterprise Multi-Agent AI Assistant

> ✨ A plug-and-play multi-agent system built with [LangGraph](https://github.com/langchain-ai/langgraph), integrating GitHub, Email, and SAP Analytics Cloud data sources. Designed for enterprise use cases and agent-to-agent collaboration.

---
<img width="1429" alt="Screenshot 2025-04-16 at 7 48 53 PM" src="https://github.com/user-attachments/assets/9fa8d681-4fdc-4d8d-bfc5-93c56f75fa76" />

<img width="1425" alt="Screenshot 2025-04-16 at 7 42 52 PM" src="https://github.com/user-attachments/assets/73de2b8e-62ef-4409-840d-74a8e3bf7d35" />

---

## Architecture
![ChatGPT Image Apr 16, 2025 at 08_00_08 PM](https://github.com/user-attachments/assets/519b3597-f2fe-44fc-a2ff-6dbe86397ecb)



## 🧩 Why This Matters

Modern enterprise environments have **fragmented data** across:
- Codebases (GitHub)
- Internal communications (Email)
- BI Dashboards (SAP Analytics Cloud)

This system shows how **independent AI agents** can be **plugged in like LEGO blocks** to:
- 🧠 Understand business context
- 🔀 Collaborate via a router node
- 💡 Deliver actionable insights instantly
- With just few lines of code - this Agent can work with your enterprise application

---

## 🔌 Plug & Play Architecture

| Agent | What It Does | How to Extend |
|-------|--------------|---------------|
| `📦 GitHub Agent` | Compares code changes across commits and summarizes impact | Point it to any repo |
| `📬 Email Agent` | Fetches and summarizes key email threads from multiple accounts | Add new inboxes in seconds |
| `📊 Analytics Agent` | Uses SAP Analytics Cloud dashboard through OAuth plugging and answers business queries | Works with any 3rd party website allowing OAuth APIs  |
| `📁 Repo List Agent` | Lists available GitHub repositories on the fly | Extend to Bitbucket or GitLab |
| `🧠 Router` | Smart dispatcher that routes user intent to the right agent | Add new agents with one routing line |

---

## 💬 What You Can Ask

> "Show me the last 10 commits from the EmailAgent repo"  
> "Fetch and summarize my latest emails"  
> "List all repositories in my GitHub account"  
> "From the SAP Analytics Cloud story, what's the sales trend?"  
> "Which product performed best in Q4?"

---

## 🎯 Key Features

- ✅ Modular, agent-based design (easily extensible)
- ✅ LangGraph orchestration with conditional routing
- ✅ Chat + memory ready
- ✅ SAP Analytics Cloud insights via API 
- ✅ Email summarization with multi-account support
- ✅ GitHub diff summarizer with next-step suggestions
- ✅ Streamlit interface (easy to demo)

---

## 🖼️ Screenshots

<img width="1418" alt="Screenshot 2025-04-16 at 7 49 40 PM" src="https://github.com/user-attachments/assets/13285f24-ece7-49e7-9280-06983cf103c6" />

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/MultiAgent_System.git
cd MultiAgent_System
pip install -r requirements.txt
streamlit run app.py
