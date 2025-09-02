from pypdf import PdfReader

def analyze_resume(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return {"raw_text": text}
