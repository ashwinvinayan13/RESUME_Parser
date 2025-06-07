from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz #for reading pdf's
import docx #for reading docx files
import re
from io import BytesIO


app = FastAPI()

SKILLS = [
    "python", "java", "c++", "django", "fastapi", "flask", "html", "css", "javascript", "react", "sql", "postgresql", "mongodb", "git", "docker", "linux",
    "pandas", "numpy", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch"
]


def extract_skill_from_text(text: str, skills_list: list[str]) -> list[str]:
    text_lower = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills

def extract_pdf(file):
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_doc(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        content = await file.read()
        text = extract_pdf(content)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        content = await file.read()
        file_like = BytesIO(content)
        text = extract_doc(file_like)
    else:
        raise HTTPException(status_code=400, detail="Unsupported File Type")
    return {"text": text}