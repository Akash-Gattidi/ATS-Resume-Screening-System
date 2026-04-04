import os
import csv
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

resumes_folder = "data/"
required_skills = ["Python", "Java", "Machine Learning", "MySQL", "React"]
results = []

# Process resumes
for file in os.listdir(resumes_folder):
    if file.endswith(".pdf"):
        resume_path = os.path.join(resumes_folder, file)
        text = extract_text_from_pdf(resume_path)
        cleaned_text = clean_text(text)
        matched_skills, score = match_skills(cleaned_text, required_skills)
        results.append({
            "Resume": file,
            "Matched Skills": ", ".join(matched_skills),
            "Score": score
        })

# Step: Rank resumes by score (highest first)
results.sort(key=lambda x: x["Score"], reverse=True)

# Save to CSV
output_file = "screening_results.csv"
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["Resume", "Matched Skills", "Score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\nScreening complete! Results saved to {output_file}")