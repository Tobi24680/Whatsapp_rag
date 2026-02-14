from pypdf import PdfReader


def extract_text_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_image(file_path: str) -> str:
    # OCR disabled on Render free tier
    return "Image text extraction is currently disabled."
