import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
from config import API_KEY 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

#  CORE RAG UTILITIES 

def chunk_text(text):
    """Chunks text extracted from PDFs to fit neatly within context windows."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(text)

def retrieve_relevant_context(query, document_text, top_k=2):
    if not document_text:
        return ""
    
    chunks = chunk_text(document_text)
    query_words = set(query.lower().split())
    
    scored_chunks = []
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.lower())
        scored_chunks.append((score, chunk))
    
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for score, chunk in scored_chunks[:top_k]]
    
    return "\n\n---\n\n".join(top_chunks)


# AGENT FLOW ARCHITECTURE 

def analyze_resume(text):
    prompt = f"""
    You are an expert Resume Profile Analyzer Agent. Analyze the following candidate text:
    {text}
    Provide a professional summary of their:
    1. Core Technical Skills
    2. Professional Strengths
    3. Weaknesses or missing metrics
    """
    response = model.generate_content(prompt)
    return response.text

def skill_gap_analysis(resume_text, job_description):
    prompt = f"""
    You are an AI Skill Gap Analyzer Agent. 
    Cross-reference the resume content against the expectations of the job description.
    
    Resume: {resume_text}
    Job Description: {job_description}
    
    Provide a bulleted summary of specific tools, languages, and methodologies missing from the resume.
    """
    response = model.generate_content(prompt)
    return response.text

def match_resume(resume_text, job_description):
    prompt = f"""
    You are an ATS Selection Optimizer Agent. Compare the resume to the job description:
    Resume: {resume_text}
    Job Description: {job_description}
    
    Provide an estimated ATS match percentage score and explicit modifications to make it match better.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_roadmap(role):
    prompt = f"""
    Create a highly specific, linear progress tracking timeline roadmap to become a professional {role}.
    Format it cleanly with directional arrows (e.g., Skill A -> Project B -> Skill C).
    """
    response = model.generate_content(prompt)
    return response.text


# CONVERSATION MEMORY CHAT

def get_mock_interview_response(raw_chat_history, resume_context="", jd_context=""):
    """
    Accepts raw database history list: [(question, answer), ...]
    Ordered from newest to oldest.
    """
    formatted_context = []
    
    if raw_chat_history:
        for q, a in reversed(raw_chat_history):
            if q:
                formatted_context.append(f"Interviewer: {q}")
            if a:
                formatted_context.append(f"Candidate: {a}")
    
    history_block = "\n".join(formatted_context)
    
    rag_resume = retrieve_relevant_context("skills experience projects technology", resume_context, top_k=2)
    rag_jd = retrieve_relevant_context("requirements duties responsibilities qualifications", jd_context, top_k=2)
    
    if not history_block.strip():
        system_instruction = (
            "This is the very start of the mock interview. You must warmly greet the candidate, "
            "introduce yourself as their Elite Technical Interviewer, and ask a challenging technical question "
            "directly customized to their resume profile or the target job description snippets provided below."
        )
    else:
        system_instruction = (
            "The candidate has responded to your previous question. Briefly critique their answer concisely "
            "(point out what was strong or correct any factual mistakes), and ask the next logical technical follow-up question."
        )
    
    prompt = f"""
    You are an Elite Technical Interviewer conducting a professional tech interview.
    
    CRITICAL ACTION INSTRUCTION:
    {system_instruction}
    
    GROUNDING RAG CONTEXT:
    [Resume Context]: {rag_resume if rag_resume else "Not provided"}
    [Target Job Context]: {rag_jd if rag_jd else "Not provided"}
    
    CONVERSATION HISTORY SO FAR:
    {history_block if history_block else "None. (This is the start of the interview)"}
    
    RULES:
    - Ask only ONE clear technical question at a time.
    - Do not output a list of questions.
    - Stay in character as a professional interviewer.
    
    Provide your next response as the Interviewer:
    """
    response = model.generate_content(prompt)
    return response.text
def evaluate_answer(answer, history):
    prompt = f"""
You are an interviewer.

Previous conversation:

{history}

Current answer:

{answer}

1. Evaluate answer.
2. Give feedback.
3. Ask one follow-up question.
"""
    response = model.generate_content(prompt)
    return response.text

def Career_Chatbot(question, resume_text=""):
    prompt = f"""
You are an AI Career Assistant.

Resume Context:
{resume_text}

Question:
{question}

Provide a helpful career-focused answer.
"""
    response = model.generate_content(prompt)
    return response.text