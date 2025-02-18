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