import os
import requests
import json
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

app = Flask(__name__)

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Directory to store temporary images
TEMP_IMAGE_DIR = Path("temp_images")
TEMP_IMAGE_DIR.mkdir(exist_ok=True)

# Path to your credentials and token files
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'


def get_credentials():
    """Handles authentication and returns the Google Drive credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return creds


def upload_to_drive(file_path, filename):
    """Uploads a file to Google Drive and returns the file URL."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Upload image to Google Drive
    file_metadata = {'name': filename}
    media = MediaFileUpload(file_path, mimetype='image/png')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Get the file URL
    file_url = f'https://drive.google.com/uc?id={file["id"]}'
    return file_url


# Endpoint to serve images
@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(TEMP_IMAGE_DIR, filename)


# Helper function to clean up images older than 30 days
def clean_up_old_images():
    cutoff_date = datetime.now() - timedelta(days=30)
    for image_file in TEMP_IMAGE_DIR.iterdir():
        if image_file.is_file():
            file_creation_date = datetime.fromtimestamp(image_file.stat().st_mtime)
            if file_creation_date < cutoff_date:
                image_file.unlink()  # Delete the old image


@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    image_url = request.args.get('url')
    version = request.args.get('version', '0.2')

    if not image_url:
        return jsonify({"status": 400, "error": "Parameter 'url' is required."}), 400

    if version not in ['0.2', '0.3', '0.4']:
        return jsonify({"status": 400, "error": "Invalid 'version' parameter."}), 400

    api_url = f"https://itzpire.com/tools/photo2anime2?url={image_url}&type=version%20{version}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({"status": response.status_code, "error": "External service error."}), response.status_code

        external_data = response.json()
        external_img_url = external_data.get("img")
        duration = external_data.get("duration")

        # Download the image
        image_response = requests.get(external_img_url, stream=True)
        if image_response.status_code == 200:
            # Generate a unique filename
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = TEMP_IMAGE_DIR / filename
            with open(file_path, 'wb') as file:
                file.write(image_response.content)

            # Upload to Google Drive
            drive_url = upload_to_drive(file_path, filename)

            # Clean up old images
            clean_up_old_images()

            return jsonify({
                "result": {
                    "img": drive_url,
                    "duration": duration
                }
            })

        return jsonify({"status": 500, "error": "Failed to download image."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"status": 503, "error": f"Service unavailable: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"status": 500, "error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
