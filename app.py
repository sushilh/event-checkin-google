
from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "extreme-ability-458402-a3-2495e0b3fd12.json"
SHEET_ID = "1L2ih057w37xAkgL2bkP600iYpDyj215R6ZDjXniLIao"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

HEADERS = ['name', 'email', 'attendees', 'allergy', 'checked_in', 'checked_in_count']

def get_all_records():
    return sheet.get_all_records()

def find_row_index_by_email(email):
    emails = sheet.col_values(2)
    for i, val in enumerate(emails):
        if val.strip().lower() == email.strip().lower():
            return i + 1
    return None

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/attendees", methods=["GET"])
def get_attendees():
    return jsonify(get_all_records())

@app.route("/add", methods=["POST"])
def add_guest():
    data = request.get_json()
    row = [
        data.get("name", ""),
        data.get("email", ""),
        data.get("attendees", 0),
        data.get("allergy", ""),
        "no",
        0
    ]
    sheet.append_row(row)
    return jsonify({"message": "Guest added successfully."})

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    row_idx = find_row_index_by_email(data.get("email"))
    if row_idx:
        sheet.update_cell(row_idx, 5, data.get("checked_in", "no"))
        sheet.update_cell(row_idx, 6, data.get("checked_in_count", 0))
        return jsonify({"message": "Check-in updated."})
    return jsonify({"error": "Email not found"}), 404

@app.route("/attendees", methods=["PUT"])
def update_attendee():
    data = request.get_json()
    row_idx = find_row_index_by_email(data.get("email"))
    if row_idx:
        col = 3 if data.get("type") == "attendees" else 6
        sheet.update_cell(row_idx, col, data.get("value"))
        return jsonify({"message": f"{data.get('type')} updated."})
    return jsonify({"error": "Email not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
