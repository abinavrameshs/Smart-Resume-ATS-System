import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
import logging

from prompts import ANALYSE_RESUME_PROMPT, SKILL_GAP_RECOMMENDATIONS_PROMPT
from utils import read_file, clear_directory, create_directory, timing

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
