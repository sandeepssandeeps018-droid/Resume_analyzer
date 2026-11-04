import google.generativeai as genai

from config import API_KEY 

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def resume_agent(resume_text):

    prompt = f"""
Analyze this resume.

Extract:

1. Skills
2. Projects
3. Education
4. Experience

Resume:
{resume_text}
"""

    response = model.generate_content(
        prompt
    )

    return response.text
def skill_gap_agent(
    resume_text,
    jd_text
):

    prompt = f"""
Compare resume and job description.

Resume:
{resume_text}

Job Description:
{jd_text}

Find:

1. Missing Skills
2. Missing Tools
3. Missing Certifications
"""

    response = model.generate_content(
        prompt
    )

    return response.text
def interview_agent(
    resume_text,
    jd_text
):

    prompt = f"""
Generate 10 interview questions.

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(
        prompt
    )

    return response.text
def roadmap_agent(
    role,
    skills
):

    prompt = f"""
Current Skills:

{skills}

Target Role:

{role}

Create a learning roadmap.
"""

    response = model.generate_content(
        prompt
    )

    return response.text
def run_agents(
    resume_text,
    jd_text,
    role
):

    resume_result = resume_agent(
        resume_text
    )

    gap_result = skill_gap_agent(
        resume_text,
        jd_text
    )

    interview_result = interview_agent(
        resume_text,
        jd_text
    )

    roadmap_result = roadmap_agent(
        role,
        resume_result
    )

    return {
        "resume": resume_result,
        "gap": gap_result,
        "interview": interview_result,
        "roadmap": roadmap_result
    }