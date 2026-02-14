from pypdf import PdfReader
from PIL import Image
import pytesseract


def extract_text_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_text_image(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)
