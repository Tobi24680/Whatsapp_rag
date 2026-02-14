import os
import requests
from fastapi import APIRouter, Request
from dotenv import load_dotenv
from twilio.rest import Client

from app.upload import extract_text_pdf
from app.rag_engine import create_vector_db, rag_answer

load_dotenv()

router = APIRouter()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def download_file(url: str, path: str):
    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)


def send_whatsapp_message(to: str, message: str):
    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=to,
        body=message
    )


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.form()

    user_no = data.get("From")
    message = data.get("Body")
    media_url = data.get("MediaUrl0")

    # 📄 Document upload
    if media_url:
        file_path = f"{UPLOAD_DIR}/{user_no}.pdf"
        download_file(media_url, file_path)

        text = extract_text_pdf(file_path)
        create_vector_db(text, user_no)

        send_whatsapp_message(
            user_no,
            "✅ Document processed successfully. You can now ask questions."
        )
        return {"status": "document processed"}

    # ❓ Question
    if message:
        try:
            answer = rag_answer(message, user_no)
        except Exception:
            answer = "❌ Please upload a document first."

        send_whatsapp_message(user_no, answer)
        return {"status": "answered"}

    return {"status": "ignored"}
