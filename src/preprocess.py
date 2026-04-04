# src/preprocess.py
import re

def clean_text(text):
    """
    Clean and normalize resume text.
    """
    text = text.lower()  # lowercase
    text = re.sub(r'\s+', ' ', text)  # normalize spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove punctuation/special chars
    return text.strip()