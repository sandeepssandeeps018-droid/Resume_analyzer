# 🚀 AI Career Copilot

An AI-powered career preparation app that helps students and job seekers analyze resumes, match them against job descriptions, find skill gaps, generate learning roadmaps, and practice with an AI mock interviewer.

Built with **Streamlit**, **Google Gemini 2.5 Flash**, **LangChain**, **FAISS**, and **SQLite**.

---

## 📌 Problem Statement

Students preparing for placements usually have to jump between many platforms for resume feedback, interview practice, and career guidance. The process is time-consuming and generic.

AI Career Copilot brings these tools into one place and personalizes them using the user's own resume and target job description.

---

## ✨ Features

| Feature | What it does |
|---|---|
| **Resume Analyzer** | Upload a PDF resume and get a summary of core skills, strengths, and weaknesses or missing metrics |
| **Job Matcher** | Compare a resume with a job description and get an estimated ATS match score plus suggested changes |
| **Skill Gap Analysis** | Lists tools, languages, and methodologies the job requires that the resume is missing |
| **Mock Interview** | Chat-based AI interviewer that asks one technical question at a time, grounded in your resume and the job description, and remembers the conversation |
| **Roadmap Generator** | Generates a step-by-step learning roadmap for a target role |
| **AI Agent Workflow** | Runs four specialized AI agents in sequence: resume extraction, skill gap, interview questions, and roadmap |
| **Career Chatbot (RAG)** | Ask questions about your resume; answers are grounded in retrieved resume chunks |

---

## 🏗️ System Architecture

```text
                ┌─────────────────────────┐
                │   Streamlit UI (app.py) │
                └────────────┬────────────┘
                             │
      ┌──────────────┬───────┴────────┬───────────────┐
      ▼              ▼                ▼               ▼
┌───────────┐  ┌────────────┐  ┌─────────────┐  ┌───────────┐
│ backend.py│  │  agent.py  │  │   rag.py    │  │ utils.py  │
│ single-   │  │ 4-step     │  │ chunk →     │  │ PDF text  │
│ call LLM  │  │ agent      │  │ embed →     │  │ extraction│
│ features +│  │ pipeline   │  │ FAISS →     │  │ (pypdf)   │
│ interview │  │            │  │ retrieve    │  │           │
└─────┬─────┘  └─────┬──────┘  └──────┬──────┘  └───────────┘
      │              │                │
      └──────────────┴───────┬────────┘
                             ▼
                  ┌─────────────────────┐
                  │  Gemini 2.5 Flash   │
                  │  gemini-embedding-  │
                  │  001 (embeddings)   │
                  └─────────────────────┘

      ┌────────────────────────────────┐
      │ database.py → SQLite (career.db)│
      │  • analysis                     │
      │  • chat_history                 │
      └────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core language |
| Streamlit | Web UI, chat interface, session state |
| Google Gemini 2.5 Flash (`google-generativeai`) | Text generation for all features |
| `gemini-embedding-001` | Text embeddings for RAG |
| LangChain (`langchain-text-splitters`, `langchain-google-genai`, `langchain-community`) | Chunking, embedding wrapper, FAISS integration |
| FAISS | In-memory vector similarity search |
| SQLite | Stores analysis results and interview chat history |
| pypdf | Extracts text from PDF resumes |

---

## 📂 Project Structure

```text
AI-Career-Copilot/
│
├── app.py          # Streamlit UI and page routing
├── backend.py      # Resume analysis, ATS match, skill gap, roadmap, mock interview logic
├── agent.py        # Four-step agent workflow (resume → gap → interview → roadmap)
├── rag.py          # RAG pipeline: chunking, embeddings, FAISS, answer generation
├── database.py     # SQLite setup and save/fetch helpers
├── utils.py        # PDF text extraction
├── config.py       # Loads the Gemini API key
│
├── career.db       # SQLite database (auto-created)
├── .env            # Your API key (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.11 or later
- A Google Gemini API key from https://aistudio.google.com/apikey

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Career-Copilot.git
cd AI-Career-Copilot
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install streamlit google-generativeai langchain-text-splitters \
            langchain-google-genai langchain-community faiss-cpu \
            pypdf python-dotenv
```
Or, once you have a `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key
```

Update `config.py` so the key is read from the environment instead of being hardcoded:
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
```

Add this to `.gitignore`:
```text
.env
venv/
career.db
__pycache__/
```

> ⚠️ **Never commit your API key.** If a key was ever pushed to GitHub, revoke it and create a new one.

### 5. Run the app
```bash
python -m streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## 🔄 How It Works

### Resume features
1. The user uploads a PDF resume.
2. `pypdf` extracts the text.
3. The text (plus the job description, when needed) is placed into a role-based prompt and sent to Gemini 2.5 Flash.
4. The response is displayed in the UI. Resume Analyzer results are also saved to SQLite.

### RAG Career Chatbot
1. Resume text is split into chunks (1000 characters, 200 overlap) using `RecursiveCharacterTextSplitter`.
2. Each chunk is embedded with `gemini-embedding-001` and stored in a FAISS index.
3. For each question, the top 3 most similar chunks are retrieved.
4. Gemini answers using only that retrieved context.

### Mock Interview
1. Interview turns are stored in the `chat_history` table.
2. On each turn, the last 10 turns are loaded and rebuilt into the prompt as conversation history.
3. Relevant resume and job description snippets are selected with keyword-overlap retrieval (top 2 chunks each).
4. Gemini plays the interviewer: greets and asks a question at the start, then critiques and asks a follow-up on later turns.

### AI Agent Workflow
Four specialized prompts run in sequence:
1. **Resume Agent**: extracts skills, projects, education, experience
2. **Skill Gap Agent**: finds missing skills, tools, certifications
3. **Interview Agent**: generates 10 tailored interview questions
4. **Roadmap Agent**: builds a learning roadmap from the extracted resume information

---

## ⚠️ Known Limitations

- Only text-based PDFs are supported (scanned PDFs need OCR).
- The ATS score is an LLM estimate, so it can vary between runs.
- The agents are a prompt-chaining pipeline, not autonomous tool-using agents.
- Mock interview history is shared globally and has no "new interview" reset.
- The FAISS index is in-memory and is lost when the app restarts.
- No user authentication; all data lives in one SQLite file.
- API calls have no retry or rate-limit handling yet.

---

## 🎯 Future Enhancements

- Fix mock interview answer handling and add a "New Interview" button with a final performance scorecard
- Structured (JSON) outputs validated with Pydantic
- LangGraph-based multi-agent orchestration
- Persistent vector store (ChromaDB or pgvector)
- FastAPI backend separated from the Streamlit frontend
- User accounts and per-user history
- Company intelligence and interview experience agents
- Personalized DSA preparation coach
- Voice-based mock interviews
- Docker deployment and CI/CD with GitHub Actions

---

## 🔐 Privacy Note

Resume text is sent to the Google Gemini API for processing. Avoid uploading resumes containing sensitive personal information you are not comfortable sharing with a third-party service.

---

## 📄 License

This project is intended for educational and research purposes.
