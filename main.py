from src.parser import extract_text_from_pdf
from src.preprocess import clean_text
from src.matcher import match_skills

resume_path = "data/resume.pdf"

text = extract_text_from_pdf(resume_path)

print("Extracted Text:\n")
print(text)