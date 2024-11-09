import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta

app = Flask(__name__)

# Directory to store temporary images (use /tmp for serverless environments like Vercel)
TEMP_IMAGE_DIR = '/tmp/temp_images'
if not os.path.exists(TEMP_IMAGE_DIR):
    os.makedirs(TEMP_IMAGE_DIR)

# Endpoint to serve images
@app.route('/tmp/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(TEMP_IMAGE_DIR, filename)

# Helper function to clean up images older than 30 days
def clean_up_old_images():
    cutoff_date = datetime.now() - timedelta(days=30)
    for image_file in os.listdir(TEMP_IMAGE_DIR):
        image_path = os.path.join(TEMP_IMAGE_DIR, image_file)
        if os.path.isfile(image_path):
            file_creation_date = datetime.fromtimestamp(os.path.getmtime(image_path))
            if file_creation_date < cutoff_date:
                os.remove(image_path)  # Delete the old image

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
            file_path = os.path.join(TEMP_IMAGE_DIR, filename)
            with open(file_path, 'wb') as file:
                file.write(image_response.content)

            # Clean up old images
            clean_up_old_images()

            # Serve the image via your domain
            served_img_url = f"https://www.youga.my.id/tmp/{filename}"

            return jsonify({
                "result": {
                    "img": served_img_url,
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
