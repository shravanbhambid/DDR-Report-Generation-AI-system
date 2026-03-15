import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a given PDF file."""
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"
    
    text_content = []
    try:
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content.append(page.get_text())
        return "\n".join(text_content)
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

def extract_text_from_file(file_path: str) -> str:
    """Reads text from a file (handles .txt or .pdf)."""
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {file_path}: {e}"
