# 🤖 Enterprise Multi-Agent AI Assistant

> ✨ A plug-and-play multi-agent system built with [LangGraph](https://github.com/langchain-ai/langgraph), integrating GitHub, Email, and SAP Analytics Cloud data sources. Designed for enterprise use cases and agent-to-agent collaboration.

---

![Insert Demo Screenshot Here](insert_screenshot_here.png)

---

## 🧩 Why This Matters

Modern enterprise environments have **fragmented data** across:
- Codebases (GitHub)
- Internal communications (Email)
- BI Dashboards (SAP Analytics Cloud)

This system shows how **independent AI agents** can be **plugged in like LEGO blocks** to:
- 🧠 Understand business context
- 🔀 Collaborate via a router node
- 💡 Deliver actionable insights instantly

---

## 🔌 Plug & Play Architecture

| Agent | What It Does | How to Extend |
|-------|--------------|---------------|
| `📦 GitHub Agent` | Compares code changes across commits and summarizes impact | Point it to any repo |
| `📬 Email Agent` | Fetches and summarizes key email threads from multiple accounts | Add new inboxes in seconds |
| `📊 SAP PDF Agent` | Parses exported SAP Analytics Cloud PDFs and answers business queries | Works with any PDF insight report |
| `📁 Repo List Agent` | Lists available GitHub repositories on the fly | Extend to Bitbucket or GitLab |
| `🧠 Router` | Smart dispatcher that routes user intent to the right agent | Add new agents with one routing line |

---

## 💬 What You Can Ask

> "Show me the last 10 commits from the EmailAgent repo"  
> "Fetch and summarize my latest emails"  
> "List all repositories in my GitHub account"  
> "From this SAP PDF, what's the sales trend?"  
> "Which product performed best in Q4?"

---

## 🎯 Key Features

- ✅ Modular, agent-based design (easily extensible)
- ✅ LangGraph orchestration with conditional routing
- ✅ Chat + memory ready
- ✅ SAP Analytics Cloud insights via PDF parsing
- ✅ Email summarization with multi-account support
- ✅ GitHub diff summarizer with next-step suggestions
- ✅ Streamlit interface (easy to demo)

---

## 🖼️ Screenshots

> 📌 *Insert demo screenshots here of:*
- Agent selection via natural language
- GitHub diff summary output
- Email digest
- SAP PDF response to a sales query

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/MultiAgent_System.git
cd MultiAgent_System
pip install -r requirements.txt
streamlit run app.py
