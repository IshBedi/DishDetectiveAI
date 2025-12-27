"""hi"""

from __future__ import print_function
import io
import os
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = None

    # Load saved OAuth token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Authenticate if needed
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('Software\client_secret_1090802411336-7m0n6u1t2h3r14epqdojovn5haubf45i.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def download_file_content(service, file_name):
    # Search for file by name
    results = service.files().list(
        q=f"name='{file_name}'",
        fields="files(id, name)"
    ).execute()

    items = results.get('files', [])

    if not items:
        print("Google Drive: names.txt not found.")
        return None

    file_id = items[0]['id']

    # Download content
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return fh.getvalue().decode("utf-8")


# ----------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------

service = get_drive_service()

print("Watching Google Drive names.txt for new lines...\n")

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
local_path = os.path.join(SCRIPT_DIR, "names.txt")

# Load current local file (to avoid writing duplicates)
local_lines = set()

# create file if missing
if not os.path.exists(local_path):
    open(local_path, "w").close()

with open(local_path, "r") as f:
    for line in f:
        local_lines.add(line.strip())

while True:
    drive_text = download_file_content(service, "names.txt")

    if drive_text:
        drive_lines = drive_text.strip().split("\n")

        for line in drive_lines:
            clean = line.strip()
            if clean and clean not in local_lines:
                # Append new line to local names.txt
                with open(local_path, "a") as lf:
                    lf.write(clean + "\n")

                print(f"New Line Added → {clean}")
                local_lines.add(clean)

    print("Checked... waiting 10 seconds.\n")
    time.sleep(10)
