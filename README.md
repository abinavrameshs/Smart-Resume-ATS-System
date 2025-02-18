# Smart-Resume-ATS-System

Smart Resume ATS System (Applicant Tracking System) using LLMs from Google

## Description

This project is a Smart Resume ATS (Applicant Tracking System) that leverages Google's Language Models (LLMs) to analyze resumes and provide detailed summaries, skill gap analyses, and recommendations. The system is built using Streamlit for the user interface and integrates with Google's GenAI for content generation.

## Features

- **Resume Analysis**: Upload a PDF resume and get a concise summary highlighting key skills, experience, education, and achievements.
- **Skill Gap Analysis**: Compare the resume against a job description to identify missing or underdeveloped skills and receive recommendations for improvement.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/abinavrameshs/Smart-Resume-ATS-System.git
    cd Smart-Resume-ATS-System
    ```

2. **Install dependencies**:
    This project uses PDM for dependency management. Ensure you have PDM installed, then run:
    ```sh
    pdm install
    ```

3. **Set up environment variables**:
    Create a [.env](http://_vscodecontentref_/1) file in the root directory and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. **Run the application**:
    ```sh
    pdm run streamlit run app.py
    ```

2. **Upload your resume**:
    - Open the application in your browser (usually at `http://localhost:8501`).
    - Upload your resume in PDF format.

3. **Analyze the resume**:
    - Click on "Resume Analysis" to get a summary of the resume.
    - Enter a job description and click on "Skill Gap Analysis and Recommendations" to identify skill gaps and get recommendations.

## Project Structure

- [app.py](app.py): Main application file containing the Streamlit interface and functions for resume analysis.
- [pyproject.toml](pyproject.toml): Project configuration file.
- [pdm.lock](pdm.lock): Lock file for dependencies.
- [README.md](README.md): Project documentation.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Author

- **Abinav Ramesh** - [abinavrameshs@gmail.com](mailto:abinavrameshs@gmail.com)
