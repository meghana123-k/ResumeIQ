import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    else:
        return "Unsupported file format"
    return clean_text(raw_text)

def clean_text(text):
    # Remove (cid:xxx) artifacts
    text = re.sub(r"\(cid:\d+\)", " ", text)

    # Normalize spaces but preserve newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    # Remove non-ASCII characters
    text = text.encode("ascii", errors="ignore").decode()

    # Normalize common tech keywords (CONTROLLED FIX)
    replacements = {
        "Java Script": "JavaScript",
        "Ja va Script": "JavaScript",
        "My SQL": "MySQL",
        "Mo ngo DB": "MongoDB",
        "Mongo DB": "MongoDB",
        "Git Hub": "GitHub",
        "backendlogic": "backend logic",
        "databasequeries": "database queries",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text.strip()
