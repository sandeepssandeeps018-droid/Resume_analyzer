import streamlit as st

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide"
)

from rag import (
    create_vector_store,
    rag_answer
)

from agent import (run_agents)

from backend import (
    analyze_resume,
    match_resume,
    generate_roadmap,
    skill_gap_analysis,
    get_mock_interview_response,
    evaluate_answer,
    Career_Chatbot
)
from database import (
    save_result,
    save_chat,
    get_chat_history
)
from utils import extract_text 

if "global_resume_text" not in st.session_state:
    st.session_state.global_resume_text = ""
if "global_jd_text" not in st.session_state:
    st.session_state.global_jd_text = ""
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

st.title("🚀 AI Career Copilot")

page = st.sidebar.selectbox(
    "Select Feature",
    [
        "Resume Analyzer",
        "Job Matcher",
        "Skill Gap Analysis",
        "Mock Interview",
        "Roadmap Generator",
        "AI Agent Workflow",
        "career chatbot"
    ]
)

if page == "Resume Analyzer":
    st.header("🕵️‍♂️ Agent 1: Resume Profile Analyzer")
    resume = st.file_uploader("Upload Resume", type=["pdf"], key="analyzer_uploader")
    
    if st.button("Analyze Resume", key="analyze_resume_btn"):
        if resume is not None:
            resume_text = extract_text(resume)
            st.session_state.global_resume_text = resume_text  
            
            with st.spinner("Analyzing text chunks..."):
                result = analyze_resume(resume_text)
                save_result(result)
                st.success("Resume Analyzed successfully!")
                st.markdown(result)
        else:
            st.error("Please upload a PDF resume first.")

elif page == "Job Matcher":
    st.header("🎯 ATS Job Matcher")
    col1, col2 = st.columns(2)
    with col1:
        resume = st.file_uploader("Upload Resume", type=["pdf"], key="matcher_resume")
    with col2:
        jd = st.text_area("Paste Job Description", key="matcher_jd")

    if st.button("Match Resume", key="match_resume_btn"):
        if resume and jd:
            resume_text = extract_text(resume)
            st.session_state.global_resume_text = resume_text
            st.session_state.global_jd_text = jd
            
            with st.spinner("Calculating matching thresholds..."):
                result = match_resume(resume_text, jd) 
                st.success("Matching Completed!")
                st.markdown(result)
        else:
            st.error("Please provide both a resume file and a job description.")

elif page == "Skill Gap Analysis":
    st.header("📊 Agent 2: Skill Gap Analyzer")
    col1, col2 = st.columns(2)
    with col1:
        resume = st.file_uploader("Upload Resume", type=["pdf"], key="gap_resume")
    with col2:
        jd = st.text_area("Paste Job Description", key="gap_jd")

    if st.button("Analyze Skill Gap", key="skill_gap_btn"):
        if resume and jd:
            resume_text = extract_text(resume)
            st.session_state.global_resume_text = resume_text
            st.session_state.global_jd_text = jd
            
            with st.spinner("Cross-referencing technology frameworks..."):
                result = skill_gap_analysis(resume_text, jd)
                st.success("Skill Gap Assessment Complete!")
                st.markdown(result)
        else:
            st.error("Please provide both a resume and a job description.")

elif page == "Mock Interview":
    st.header("🤖 Interactive AI Mock Interview")
    
    # Fetch chat history (returns list of tuples: [(question, answer), ...] ordered DESC)
    raw_history = get_chat_history()
    
    # 1. Render all past conversation items to the chat window UI
    for q, a in reversed(raw_history):
        if q:
            st.chat_message("assistant").write(q)
        if a:
            st.chat_message("user").write(a)

    # 2. If no history exists at all, generate the first question automatically
    if len(raw_history) == 0:
        with st.spinner("Initializing your interviewer..."):
            first_question = get_mock_interview_response(
                raw_chat_history=[], 
                resume_context=st.session_state.get("global_resume_text", ""), 
                jd_context=st.session_state.get("global_jd_text", "")
            )
            # Save to database so it populates the raw_history on the next pass
            save_chat(first_question, "")
            # Immediately rerun the app to draw the question on the screen
            st.rerun()

    # 3. Accept user response answers
    user_answer = st.chat_input("Type your answer here...")
    if user_answer:
        # Display candidate answer on screen immediately
        st.chat_message("user").write(user_answer)
        
        with st.spinner("Interviewer is evaluating your response..."):
            # Request the next question from the backend agent
            next_question = get_mock_interview_response(
                raw_chat_history=raw_history,
                resume_context=st.session_state.get("global_resume_text", ""),
                jd_context=st.session_state.get("global_jd_text", "")
            )
            
            # Save this round to the database
            save_chat(next_question, user_answer)
            # Refresh screen layout to render the new dialog pair sequentially
            st.rerun()
    # 3. Process candidate input answers
    
    if user_answer:
        # Display candidate answer on screen immediately
        st.chat_message("user").write(user_answer)
        
        with st.spinner("Evaluating and preparing follow-up..."):
            # Request follow-up question from our updated backend agent
            next_question = get_mock_interview_response(
                raw_chat_history=raw_history,
                resume_context=st.session_state.get("global_resume_text", ""),
                jd_context=st.session_state.get("global_jd_text", "")
            )
            
            # Save the exchange to your database
            save_chat(next_question, user_answer)
            # Refresh page to maintain proper display layout sequence
            st.rerun()

elif page == "Roadmap Generator":
    st.header("🗺️ Resume-to-Roadmap Generator")
    role = st.text_area(
    "Target Role",
    placeholder="Enter your target role (e.g., 'Data Scientist')",
    key="roadmap_role"
)

    if st.button("Generate Roadmap", key="roadmap_btn"):
        with st.spinner("Building path structure..."):
            result = generate_roadmap(role)
            st.success(f"Generated roadmap for {role}:")
            st.markdown(result)

elif page == "career chatbot":
    st.header("RAG Career Assistant")

    resume = st.file_uploader("Upload Resume", type=["pdf"], key="chatbot_resume_uploader")

    if resume:
        resume_text = extract_text(resume)
        if st.session_state.vector_store is None:
            with st.spinner("Indexing resume context..."):
                st.session_state.vector_store = create_vector_store(resume_text)
                st.success("Resume context successfully indexed!")

    question = st.chat_input("Ask about your resume")

    if question:
        if st.session_state.vector_store is not None:
            st.chat_message("user").write(question)
            with st.spinner("Consulting resume profile..."):
                answer = rag_answer(st.session_state.vector_store, question)
            st.chat_message("assistant").write(answer)
        else:
            st.error("Please upload a PDF resume before asking questions.")

elif page == "AI Agent Workflow":
    resume = st.file_uploader("Upload Resume", type=["pdf"])
    jd = st.text_area("Paste Job Description")
    role = st.text_input("Target Role")

    if st.button("Run Agents"):
     with st.spinner("Analyzing and generating insights..."):   
        resume_text = extract_text(resume)
        results = run_agents(resume_text, jd, role)
    

        st.subheader("Resume Analysis")
        st.write(results["resume"])
        st.subheader("Skill Gap")
        st.write(results["gap"])

        st.subheader("Interview Questions")
        st.write(results["interview"])

        st.subheader("Roadmap")
        st.write(results["roadmap"])