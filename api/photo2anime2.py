import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)

# Directory to store temporary images
TEMP_IMAGE_DIR = Path("temp_images")
TEMP_IMAGE_DIR.mkdir(exist_ok=True)

# Function to clean up images older than 30 days
def clean_up_old_images():
    cutoff_date = datetime.now() - timedelta(days=30)
    for image_file in TEMP_IMAGE_DIR.iterdir():
        if image_file.is_file():
            file_creation_date = datetime.fromtimestamp(image_file.stat().st_mtime)
            if file_creation_date < cutoff_date:
                image_file.unlink()  # Delete the old image

# Endpoint to serve images
@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(TEMP_IMAGE_DIR, filename)

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

        if not external_img_url:
            return jsonify({"status": 500, "error": "Image URL not found in the response."}), 500

        # Download the image
        image_response = requests.get(external_img_url)
        if image_response.status_code == 200:
            # Generate a unique filename
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = TEMP_IMAGE_DIR / filename

            # Save the image locally
            with open(file_path, 'wb') as file:
                file.write(image_response.content)

            # Clean up old images
            clean_up_old_images()

            # Serve the image via your domain (temporary link)
            served_img_url = f"https://www.youga.my.id/images/{filename}"

            return jsonify({
                "result": {
                    "img": served_img_url,
                    "duration": duration
                }
            })
        else:
            return jsonify({"status": 500, "error": "Failed to download image."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"status": 503, "error": f"Service unavailable: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"status": 500, "error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
