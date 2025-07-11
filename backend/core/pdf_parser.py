import io
from typing import List
import pdfplumber

def extract_chunks(pdf_bytes: bytes) -> list[str]:
    chunks = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                chunks.extend([
                    text[i:i+500]
                    for i in range(0, len(text), 500)
                    if text[i:i+500].strip()
                ])
    return chunks