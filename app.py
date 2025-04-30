from flask import Flask, request, jsonify, send_from_directory
import gspread
from google.oauth2.service_account import Credentials
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SHEET_ID = "1L2ih057w37xAkgL2bkP600iYpDyj215R6ZDjXniLIao"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet("Sheet1")

HEADERS = ['name', 'email', 'attendees', 'allergy', 'checked_in', 'checked_in_count']

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')
