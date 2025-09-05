from io import BytesIO
from typing import BinaryIO

from pypdf import PdfReader


def extract_text_from_pdf(file_like: BinaryIO) -> str:
    data = file_like.read()
    reader = PdfReader(BytesIO(data))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n\n".join(t.strip() for t in texts if t and t.strip())

