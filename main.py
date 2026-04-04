import os
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

# Folder containing resumes
resumes_folder = "data/"

# Job required skills (for now hardcoded, later from dashboard)
required_skills = ["Python", "Java", "Machine Learning", "SQL", "React"]

# Process each resume in the folder
for file in os.listdir(resumes_folder):
    if file.endswith(".pdf"):
        resume_path = os.path.join(resumes_folder, file)
        
        # Step 1: Extract text
        text = extract_text_from_pdf(resume_path)
        
        # Step 2: Clean text
        cleaned_text = clean_text(text)
        
        # Step 3: Match skills
        matched_skills, score = match_skills(cleaned_text, required_skills)
        
        # Step 4: Output
        print(f"\nResume: {file}")
        print("Matched Skills:", matched_skills)
        print("Score:", score, "%")