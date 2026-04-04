import os
import csv
from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

# Folder containing resumes
resumes_folder = "data/"

# Job required skills (for now hardcoded, later from dashboard)
required_skills = ["Python", "Java", "Machine Learning", "SQL", "React"]

# List to store results for CSV
results = []

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
        
        # Store results
        results.append({
            "Resume": file,
            "Matched Skills": ", ".join(matched_skills),
            "Score": score
        })

# Step 4: Save results to CSV
output_file = "screening_results.csv"
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["Resume", "Matched Skills", "Score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\nScreening complete! Results saved to {output_file}")