import os
import time
import requests
from io import BytesIO
from PIL import Image

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# ================= SETTINGS =================
ESP32_URL = "http://10.0.0.235/capture"

LOCAL_SAVE_DIR = "frames"
SAVE_EVERY_N = 300
CAPTURE_DELAY = 0.1  # seconds between capture attempts

GOOGLE_DRIVE_FOLDER_ID = "1dyTzArcYLBU5cF_uQuX3-DwMXtA7GTPC"
# ============================================

os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)

# -------- GOOGLE DRIVE AUTH --------
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
creds = None

script_dir = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(script_dir, "token.pickle")):
    with open(os.path.join(script_dir, "token.pickle"), "rb") as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(script_dir, "credentials.json"), SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open(os.path.join(script_dir, "token.pickle"), "wb") as token:
        pickle.dump(creds, token)

drive_service = build("drive", "v3", credentials=creds)

# -------- HELPER FUNCTIONS --------
def capture_esp32_image():
    r = requests.get(ESP32_URL, timeout=3)
    img = Image.open(BytesIO(r.content)).convert("RGB")
    return img

def upload_to_drive(filepath, filename):
    file_metadata = {
        "name": filename,
        "parents": [GOOGLE_DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(filepath, mimetype="image/jpeg")
    drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

# ================= MAIN LOOP =================
frame_count = 0

print("ESP32 → Google Drive uploader started")

while True:
    try:
        frame_count += 1

        if frame_count % SAVE_EVERY_N == 0:
            img = capture_esp32_image()
            filename = f"frame_{frame_count}.jpg"
            filepath = os.path.join(LOCAL_SAVE_DIR, filename)

            img.save(filepath)
            print(f"Captured {filename}")

            upload_to_drive(filepath, filename)
            print(f"Uploaded {filename} to Drive")

            os.remove(filepath)

        time.sleep(CAPTURE_DELAY)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)
