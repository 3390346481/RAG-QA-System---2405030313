import os
from typing import List
from PyPDF2 import PdfReader
from docx import Document

def load_pdf(file_path: str) -> str:
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF {file_path}: {str(e)}")
    return text

def load_docx(file_path: str) -> str:
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {str(e)}")
    return text

def load_document(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    else:
        print(f"Unsupported file format: {ext}")
        return ""

def load_documents_from_folder(folder_path: str) -> List[tuple]:
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in [".pdf", ".docx"]:
                text = load_document(file_path)
                if text.strip():
                    documents.append((filename, text))
    return documents

if __name__ == "__main__":
    docs = load_documents_from_folder("docs")
    print(f"Loaded {len(docs)} documents")
    for name, text in docs:
        print(f"{name}: {len(text)} characters")
