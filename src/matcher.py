# src/matcher.py

def match_skills(resume_text, required_skills):
    """
    Matches required skills in the resume and returns:
    - list of matched skills
    - simple matching score in percentage
    """
    resume_words = set(resume_text.split())
    matched = [skill for skill in required_skills if skill.lower() in resume_words]
    score = len(matched) / len(required_skills) * 100
    return matched, round(score, 2)