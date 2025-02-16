import os
import pathlib
import shutil
import streamlit as st
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import mimetypes
from functools import wraps
import logging

# Constants
MODEL_ID = "gemini-2.0-flash"
CAPTURE_FOLDER = "files"

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

# Initialize Google GenAI client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_response(
    client: genai.Client, model_id: str, contents: list
):
    try:
        response = client.models.generate_content(model=model_id, contents=contents)
        return response
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        st.error("Failed to generate response. Please try again.")
        return None


def detect_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def read_file(filepath: str) -> types.Part:
    try:
        data_bytes = types.Part.from_bytes(
            data=pathlib.Path(filepath).read_bytes(),
            mime_type=detect_mime_type(filepath),
        )
        return data_bytes
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        st.error("Failed to read file. Please try again.")
        return None


def clear_directory(folder_path: str = "files") -> None:
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")


def create_directory(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        st.write("Took: %2.4f sec" % (te - ts))
        return result

    return wrap


ANALYSE_RESUME_PROMPT = """
Task: Resume Analysis and Summarization
Analyze the attached PDF content and extract relevant information to provide a concise summary. The summary should highlight the candidate's key skills, experience, education, and achievements.

Input Requirements:
- PDF content: A PDF file containing the candidate's resume.

Output Requirements:
- Summary: A concise summary (around 100-150 words) of the candidate's resume, highlighting their key skills, experience, education, and achievements.
- Key Skills: A list of the candidate's key skills mentioned in the resume.
- Work Experience: A list of the candidate's work experience, including job titles, company names, and dates of employment.
- Education: A list of the candidate's educational qualifications, including degrees, institutions, and dates of graduation.
- Achievements: A list of the candidate's notable achievements, including awards, certifications, and publications.

Analysis Requirements:
- Entity Recognition: Identify and extract relevant entities from the resume, such as names, job titles, company names, and educational institutions.
- Part-of-Speech Tagging: Analyze the grammatical structure of the resume to identify relevant phrases and sentences.
- Dependency Parsing: Analyze the syntactic structure of the resume to identify relationships between entities.
- Semantic Role Labeling: Identify the roles played by entities in the resume, such as "applicant" or "employer".

Response Format:
Provide the output in a clear and concise format, using bullet points and headings where applicable. Include the summary, key skills, work experience, education, and achievements in separate sections.
"""

SKILL_GAP_RECOMMENDATIONS_PROMPT = """
Task: Resume Analysis and Skill Gap Identification
Analyze the attached PDF resume content with respect to the provided job description, and identify the candidate's skill gaps, top skills, and missing skills.

Input Requirements:
- PDF Resume: A PDF file containing the candidate's resume.
- Job Description: A text string containing the job description, including the required skills, qualifications, and responsibilities.

Output Requirements:
- Skill Gap Analysis: A report highlighting the candidate's skill gaps with respect to the job description, including:
    - Missing skills: A list of skills mentioned in the job description that are not present in the candidate's resume.
    - Underdeveloped skills: A list of skills mentioned in the job description that are present in the candidate's resume but require further development.
- % Match and % Mismatch: A calculation of the percentage of skills and qualifications in the job description that are matched or mismatched with the resume.
- Top Skills: A list of the candidate's top skills that match the job description, including:
    - Skill name
    - Proficiency level (e.g., beginner, intermediate, advanced)
- Missing Skills: A list of skills mentioned in the job description that are not present in the candidate's resume, including:
    - Skill name
    - Importance level (e.g., required, preferred, nice-to-have)
- Recommendations: A list of recommendations for the candidate to improve their skills and increase their chances of matching the job requirements.

Analysis Requirements:
- Entity Recognition: Identify and extract relevant entities from the resume and job description, such as skills, qualifications, and job titles.
- Part-of-Speech Tagging: Analyze the grammatical structure of the resume and job description to identify relevant phrases and sentences.
- Dependency Parsing: Analyze the syntactic structure of the resume and job description to identify relationships between entities.
- Semantic Role Labeling: Identify the roles played by entities in the resume and job description, such as "applicant" or "employer".
- Skill Matching: Match the skills mentioned in the job description with the skills mentioned in the candidate's resume, using techniques such as keyword extraction and semantic search.

Response Format:
Provide the output in a clear and concise format, using bullet points and headings where applicable. Include the skill gap analysis, top skills, missing skills, and recommendations in separate sections.
"""

# Set up the Streamlit interface
st.title("Resume Analysis Tool")

# Create a flag to indicate if the file upload was successful
file_uploaded = False

# Clear the CAPTURE_FOLDER
clear_directory(folder_path=CAPTURE_FOLDER)
# Create a directory to store the uploaded files
create_directory(CAPTURE_FOLDER)

# Upload the file and read it
file_uploader = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
if file_uploader:
    with st.spinner("Uploading file..."):
        file_path = os.path.join(CAPTURE_FOLDER, file_uploader.name)
        try:
            with open(file_path, "wb") as f:
                f.write(file_uploader.getbuffer())
            file_uploaded = True
            st.success("File uploaded successfully!")
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            st.error("Failed to upload file. Please try again.")

# Load Resume file and read content
resume_content = None
if file_uploaded:
    resume_content = read_file(file_path)

# Define a text field to input job description
job_description = st.text_area("Job Description", height=200)


# Define a function to analyze the resume
@timing
def analyze_resume(
    resume_content: types.Part, prompt: str = ANALYSE_RESUME_PROMPT
) -> None:
    if resume_content:
        output = generate_response(client, MODEL_ID, [prompt, resume_content])
        if output:
            st.markdown(output.text)


# Define a function to analyze the skill gap
@timing
def skill_gap_recommendations(
    resume_content: types.Part,
    job_description: str,
    prompt: str = SKILL_GAP_RECOMMENDATIONS_PROMPT,
) -> None:
    if resume_content and job_description:
        output = generate_response(
            client, MODEL_ID, [prompt, resume_content, job_description]
        )
        if output:
            st.write("Skill Gaps and Recommendations:")
            st.markdown(f"{output.text}")


# Create buttons for each analysis
if st.button("Resume Analysis"):
    analyze_resume(resume_content)

if st.button("Skill Gap Analysis and Recommendations"):
    skill_gap_recommendations(resume_content, job_description)
