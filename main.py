from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

resume_path = "data/resume.pdf"

text = extract_text_from_pdf(resume_path)

print("Extracted Text:\n")
print(text)

cleaned_text = clean_text(text)

# Step 3: Define job required skills
required_skills = ["Python", "Java", "Machine Learning", "SQL", "React"]

# Step 4: Match skills
matched_skills, score = match_skills(cleaned_text, required_skills)

# Step 5: Output results
print("\nMatched Skills:", matched_skills)
print("Score:", score, "%")