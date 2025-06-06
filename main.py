from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz #for reading pdf's
import docx #for reading docx files
import re
from io import BytesIO


app = FastAPI()

def extract_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
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