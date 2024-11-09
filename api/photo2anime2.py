import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Directory for temporary image storage (used in local and serverless environments)
TEMP_IMAGE_DIR = '/tmp/temp_images'

# Ensure temp directory exists
os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

# Endpoint to serve images
@app.route('/tmp/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(TEMP_IMAGE_DIR, filename)

# Helper function to clean up old images
def clean_up_old_images():
    cutoff_date = datetime.now() - timedelta(days=30)
    for image_file in Path(TEMP_IMAGE_DIR).iterdir():
        if image_file.is_file():
            file_creation_date = datetime.fromtimestamp(image_file.stat().st_mtime)
            if file_creation_date < cutoff_date:
                image_file.unlink()  # Delete the old image

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Get the URL parameter from the request
    image_url = request.args.get('url')
    version = request.args.get('version', '0.2')

    # Log the received image URL and version for debugging
    logging.debug(f"Received image_url: {image_url}, version: {version}")

    # If the URL is not provided, return an error
    if not image_url:
        return jsonify({"status": 400, "error": "Parameter 'url' is required."}), 400

    # Validate the version parameter
    if version not in ['0.2', '0.3', '0.4']:
        return jsonify({"status": 400, "error": "Invalid 'version' parameter."}), 400

    # API endpoint for processing the image (photo to anime)
    api_url = f"https://itzpire.com/tools/photo2anime2?url={image_url}&type=version%20{version}"

    try:
        # Request to the external service
        response = requests.get(api_url)
        
        # Log the response from the external API
        logging.debug(f"External API response status: {response.status_code}, response: {response.text}")

        # Check if the response is successful
        if response.status_code != 200:
            return jsonify({"status": response.status_code, "error": "External service error."}), response.status_code

        # Get the image URL from the response data
        external_data = response.json()
        external_img_url = external_data.get("img")
        duration = external_data.get("duration")

        # Log the external image URL and duration
        logging.debug(f"External image URL: {external_img_url}, duration: {duration}")

        # Download the image
        image_response = requests.get(external_img_url, stream=True)
        if image_response.status_code == 200:
            # Generate a unique filename for the image
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = os.path.join(TEMP_IMAGE_DIR, filename)
            
            # Save the image to the temporary directory
            with open(file_path, 'wb') as file:
                file.write(image_response.content)

            # Clean up old images
            clean_up_old_images()

            # Construct the URL to serve the image
            served_img_url = f"https://www.youga.my.id/tmp/{filename}"

            # Return the result in JSON format
            return jsonify({
                "result": {
                    "img": served_img_url,
                    "duration": duration
                }
            })

        return jsonify({"status": 500, "error": "Failed to download image."}), 500

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {str(e)}")
        return jsonify({"status": 503, "error": f"Service unavailable: {str(e)}"}), 503
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"status": 500, "error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
