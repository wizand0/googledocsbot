import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = {
    "type": "service_account",
    "project_id": "wide-decoder-317609",
    "private_key_id": os.getenv("PRIVATE_KEY_ID", ""),
    "private_key": os.getenv('PRIVATE_KEY', '').replace('\\n', '\n'),
    "client_email": "google-sheets-api@docs-and-telegram.iam.gserviceaccount.com",
    "client_id": os.getenv("client_id", ""),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets-api%40docs-and-telegram.iam.gserviceaccount.com"
}

TG_TOKEN = os.getenv('TG_TOKEN', '')
SHEET_ID = "18dRfN-VEm1nRGCqXwcP0yCN3hGitOD7E8ge5JJgsjeQ"
SHEET_URL = "https://docs.google.com/spreadsheets/d/18dRfN-VEm1nRGCqXwcP0yCN3hGitOD7E8ge5JJgsjeQ/edit#gid=0"