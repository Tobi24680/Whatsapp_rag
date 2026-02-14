from pypdf import PdfReader
from PIL import Image


def extract_text_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_text_image(file_path: str) -> str:
    return "Image text extraction not supported."
