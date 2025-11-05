import fitz  # PyMuPDF
import docx

def read_pdf(path):
    text_parts = []
    doc = fitz.open(path)
    for page in doc:
        txt = page.get_text()
        if txt:
            text_parts.append(txt)
    doc.close()
    return "\n".join(text_parts)

def read_docx(path):
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(paragraphs)
