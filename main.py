import os
import re
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

resumes_folder = "data/"

weights = {
    "skills": 50,
    "experience": 20,
    "education": 20,
    "certification": 10
}

def extract_experience(text):
    patterns = [
        r'(\d+)\s*\+?\s*years',
        r'(\d+)-year',
        r'(\d+)\s*yrs'
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0

def extract_education(text):
    degrees = ["B.Tech", "M.Tech", "MBA", "B.Sc", "B.E", "M.Sc"]
    for degree in degrees:
        if degree.lower() in text.lower():
            return degree
    return "Unknown"

def extract_certifications(text):
    known_certs = ["NPTEL Java", "AWS", "Scrum Master"]
    found = []
    for cert in known_certs:
        if cert.lower() in text.lower():
            found.append(cert)
    return found


# ✅ FINAL FUNCTION
def run_screening(required_skills, required_experience, desired_education):

    results = []

    for file in os.listdir(resumes_folder):
        if file.endswith(".pdf"):

            resume_path = os.path.join(resumes_folder, file)

            text = extract_text_from_pdf(resume_path)
            cleaned_text = clean_text(text)

            matched_skills, _ = match_skills(cleaned_text, required_skills)

            # Skill score
            if len(required_skills) > 0:
                skill_score = len(matched_skills) / len(required_skills) * weights["skills"]
            else:
                skill_score = 0

            exp = extract_experience(cleaned_text)
            edu = extract_education(cleaned_text)
            certs = extract_certifications(cleaned_text)

            exp_score = weights["experience"] if exp >= required_experience else 0
            edu_score = weights["education"] if edu == desired_education else 0
            cert_score = weights["certification"] if len(certs) > 0 else 0

            total_score = round(skill_score + exp_score + edu_score + cert_score, 2)

            results.append({
                "Resume": file,
                "Experience": exp,
                "Education": edu,
                "Skills": ", ".join(matched_skills),
                "Score": total_score
            })

    results.sort(key=lambda x: x["Score"], reverse=True)

    return results