import os
import json
import re
import unicodedata
import fitz  # PyMuPDF
import docx
import pandas as pd
from pathlib import Path

def clean_text(text):
    """
    Normalizes unicode characters and removes non-printable characters.
    """
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Remove non-printable characters (except standard whitespace)
    text = "".join(ch for ch in text if ch.isprintable() or ch in '\n\t\r')
    
    # Replace multiple whitespaces/newlines with single space/newline if needed
    # For now, we prefer to keep structure but just trim
    text = text.strip()
    
    return text

def extract_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def extract_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_from_xlsx(file_path):
    try:
        # Read all sheets
        xls = pd.ExcelFile(file_path)
        text = ""
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Convert dataframe to string representation
            text += f"Sheet: {sheet_name}\n"
            text += df.to_string(index=False) + "\n\n"
        return text
    except Exception as e:
        print(f"Error reading XLSX {file_path}: {e}")
        return ""

def extract_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return extract_from_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        # Note: python-docx only supports .docx. .doc support requires other tools or conversion.
        # We will try to treat it as docx or fail gracefully.
        if ext == '.docx':
            return extract_from_docx(file_path)
        else:
             return "DOC format not fully supported without conversion tools. Please convert to DOCX."
    elif ext == '.xlsx':
        return extract_from_xlsx(file_path)
    elif ext == '.txt':
        return extract_from_txt(file_path)
    else:
        return ""

def process_directory(directory_path, output_file='output.json'):
    results = []
    directory = Path(directory_path)
    
    if not directory.exists():
        return {"error": "Directory does not exist"}

    for file_path in directory.iterdir():
        if file_path.is_file():
            # Check for supported extensions to avoid processing unsupported system files
            if file_path.suffix.lower() in ['.pdf', '.docx', '.xlsx', '.txt']:
                raw_text = extract_text_from_file(str(file_path))
                cleaned = clean_text(raw_text)
                results.append({
                    "file": file_path.name,
                    "contents": cleaned
                })
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        return {"message": f"Successfully processed {len(results)} files. Output saved to {output_file}", "output_file": output_file}
    except Exception as e:
        return {"error": f"Failed to save output: {e}"}
