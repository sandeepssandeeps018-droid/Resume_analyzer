# 🚀 AI Career Copilot

### An Agentic AI-Powered Career Preparation and Interview Simulation System

AI Career Copilot is an intelligent career preparation platform designed to help students prepare for placements and technical interviews. It uses Generative AI, Retrieval-Augmented Generation (RAG), and AI agents to analyze resumes, identify skill gaps, generate personalized career roadmaps, and conduct mock interviews.

The system aims to transform traditional placement preparation into a personalized, AI-driven experience.

---

## 📌 Problem Statement

Students preparing for placements often need to search across multiple platforms for company information, interview experiences, coding questions, aptitude resources, and career guidance.

This process is time-consuming and lacks personalization.

AI Career Copilot addresses this problem by providing an integrated AI-powered platform that analyzes a student's profile and generates personalized preparation strategies based on their target company and job role.

---

## ✨ Features

### 1. Resume Analyzer
- Upload resumes in PDF format.
- Extract resume information automatically.
- Analyze technical skills and project experience.
- Identify resume strengths and weaknesses.
- Generate AI-powered improvement suggestions.

### 2. Skill Gap Analysis
- Compare candidate skills with target job requirements.
- Identify missing technical skills.
- Highlight existing strengths.
- Recommend relevant preparation topics.

### 3. Personalized Career Roadmap
- Generate structured preparation plans.
- Provide topic-wise learning recommendations.
- Suggest preparation strategies based on career goals.

### 4. AI Mock Interview
- Simulate technical and HR interviews.
- Generate context-aware interview questions.
- Evaluate candidate responses.
- Provide constructive feedback.

### 5. Interview Day Simulation
- Simulate a multi-round placement interview.
- Adapt questions based on previous answers.
- Generate a final interview performance scorecard.

### 6. Retrieval-Augmented Generation (RAG)
- Retrieve relevant information from knowledge sources.
- Improve the relevance of AI-generated responses.
- Support context-aware career guidance.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │      Streamlit       │
                 │     User Interface   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Application      │
                 │       Backend        │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ Resume     │ │ Skill Gap  │ │ Interview  │
       │ Analyzer   │ │ Agent      │ │ Agent      │
       └────────────┘ └────────────┘ └────────────┘
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                 ┌──────────────────────┐
                 │   Gemini AI Model    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   RAG / Vector DB    │
                 │      ChromaDB        │
                 └──────────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive frontend |
| FastAPI | Backend API framework |
| Google Gemini API | Generative AI |
| LangChain | RAG pipeline and document processing |
| LangGraph | Multi-agent workflow orchestration |
| ChromaDB | Vector database |
| Pydantic | Data validation |
| SQLite | Database storage |
| PyPDF | PDF text extraction |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📂 Project Structure

```text
AI-Career-Copilot/
│
├── app.py
├── agent.py
├── backend.py
├── config.py
├── database.py
├── rag.py
├── utils.py
│
├── career.db
├── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- Visual Studio Code
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Career-Copilot.git
```

Navigate to the project directory:

```bash
cd AI-Career-Copilot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Obtain your API key from:

https://aistudio.google.com/apikey

Do not upload your API key to GitHub.

### 6. Run the Application

```bash
python -m streamlit run app.py
```

The application will be available at:

http://localhost:8501

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key for Google Gemini |

---

## 🔄 Application Workflow

1. The user uploads a resume.
2. The system extracts the resume text.
3. AI analyzes the candidate's skills and experience.
4. The user selects a target company and job role.
5. The system identifies skill gaps.
6. Personalized preparation recommendations are generated.
7. The mock interview agent conducts an interview.
8. Candidate responses are evaluated.
9. A final performance scorecard is generated.

---

## 🎯 Future Enhancements

- Company Intelligence Agent for company research.
- Interview Experience Mining Agent.
- Personalized DSA preparation coach.
- Automated coding assessments.
- Real-time voice-based mock interviews.
- Interview performance analytics dashboard.
- LangGraph-based multi-agent orchestration.
- AWS deployment using Docker.
- GitHub Actions CI/CD integration.

---

## 🎓 Project Objective

The objective of AI Career Copilot is to develop an intelligent, personalized career preparation system that assists students in improving their technical skills, interview performance, and placement readiness through autonomous AI-powered assistance.

---

## 👨‍💻 Developed By

**AI Career Copilot Project Team**

Developed as an AI-powered career preparation and placement assistance project.

---

## 📄 License

This project is intended for educational and research purposes.