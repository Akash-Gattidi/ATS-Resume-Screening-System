import os
import csv
import re
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

# Folder containing resumes
resumes_folder = "data/"

# Employer requirements (demo)
required_skills = ["Python", "Java", "Machine Learning", "MySQL", "React"]
required_experience = 2  # minimum years
desired_education = ["B.Tech", "M.Tech"]
required_certifications = ["NPTEL Java"]  # optional

# Weights (percent)
weights = {
    "skills": 50,
    "experience": 20,
    "education": 20,
    "certification": 10
}

# Employer criteria for filtering
criteria = {
    "min_experience": 2,
    "education": desired_education,
    "skills": ["Python", "React"]  # must-have skills
}

# Helper functions to parse resume content

def extract_experience(text):
    """Extract total years of experience from text."""
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
    """Extract highest degree from text."""
    degrees = ["B.Tech", "M.Tech", "MBA", "B.Sc", "B.E", "M.Sc"]
    for degree in degrees:
        if degree.lower() in text.lower():
            return degree
    return "Unknown"

def extract_certifications(text):
    """Return a list of recognized certifications found in resume."""
    known_certs = ["NPTEL Java", "AWS", "Scrum Master"]
    found = []
    for cert in known_certs:
        if cert.lower() in text.lower():
            found.append(cert)
    return found

# List to store all resumes
results = []

# Process each resume
for file in os.listdir(resumes_folder):
    if file.endswith(".pdf"):
        resume_path = os.path.join(resumes_folder, file)
        text = extract_text_from_pdf(resume_path)
        cleaned_text = clean_text(text)
        
        # Step 1: Skill matching
        matched_skills, skill_match_count = match_skills(cleaned_text, required_skills)
        skill_score = len(matched_skills) / len(required_skills) * weights["skills"]

        # Step 2: Extract structured info from resume text
        exp = extract_experience(cleaned_text)
        edu = extract_education(cleaned_text)
        certs = extract_certifications(cleaned_text)

        # Step 3: Compute scores
        exp_score = weights["experience"] if exp >= required_experience else 0
        edu_score = weights["education"] if edu in desired_education else 0
        cert_score = weights["certification"] if any(c in required_certifications for c in certs) else 0

        # Total combined score
        total_score = round(skill_score + exp_score + edu_score + cert_score, 2)

        # Store resume info
        results.append({
            "Resume": file,
            "Work Experience (yrs)": exp,
            "Education": edu,
            "Matched Skills": ", ".join(matched_skills),
            "Total Score": total_score
        })

# Step 4: Filter resumes based on employer criteria
filtered_results = []
for r in results:
    if r["Work Experience (yrs)"] >= criteria["min_experience"] and \
       r["Education"] in criteria["education"] and \
       all(skill in r["Matched Skills"] for skill in criteria["skills"]):
        filtered_results.append(r)

# Step 5: Sort filtered resumes by total score (highest first)
filtered_results.sort(key=lambda x: x["Total Score"], reverse=True)

# Step 6: Save to CSV
output_file = "screening_results.csv"
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["Resume", "Work Experience (yrs)", "Education", "Matched Skills", "Total Score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in filtered_results:
        writer.writerow(row)

print(f"\nScreening complete! Filtered and ranked results saved to {output_file}")