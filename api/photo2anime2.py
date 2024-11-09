import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from urllib.parse import quote
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)

# Temporary image storage directory
TEMP_IMAGE_DIR = '/tmp/temp_images'

# Ensure the directory exists (Note: this may not be needed for serverless environments like Vercel)
if not os.path.exists(TEMP_IMAGE_DIR):
    os.makedirs(TEMP_IMAGE_DIR)

# Function to clean up old images (older than 30 days)
def clean_up_old_images():
    cutoff_date = datetime.now() - timedelta(days=30)
    for image_file in os.listdir(TEMP_IMAGE_DIR):
        file_path = os.path.join(TEMP_IMAGE_DIR, image_file)
        if os.path.isfile(file_path):
            file_creation_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_creation_date < cutoff_date:
                os.remove(file_path)

# Route to serve the generated images
@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(TEMP_IMAGE_DIR, filename)

# Helper function to convert photo to anime
def photo_to_anime(url):
    try:
        # Ensure the image URL is encoded correctly
        encoded_url = quote(url, safe='')

        # External API URL
        api_url = f"https://itzpire.com/tools/photo2anime2?url={encoded_url}&type=version%200.2"
        
        # Custom headers (optional, can help bypass any restrictions)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # Send the request to the external API
        response = requests.get(api_url, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)  # Debugging step to print the response data

            # Ensure the image URL is in the response
            if "img" in response_data:
                external_img_url = response_data["img"]
                print("Image URL found:", external_img_url)
                return external_img_url  # Return the URL of the generated image
            else:
                print("Image URL not found in the response.")
                return None
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# API endpoint to handle the conversion request
@app.route('/api/photo2anime2', methods=['GET'])
def handle_photo_to_anime():
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({"status": 400, "error": "Parameter 'url' is required."}), 400

    anime_img_url = photo_to_anime(image_url)
    
    if anime_img_url:
        # Download the generated image
        img_response = requests.get(anime_img_url)
        
        if img_response.status_code == 200:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = os.path.join(TEMP_IMAGE_DIR, filename)

            # Save the image to the temporary directory
            with open(file_path, 'wb') as file:
                file.write(img_response.content)

            # Clean up old images
            clean_up_old_images()

            # Serve the image URL to the user
            served_img_url = f"https://www.youga.my.id/images/{filename}"

            return jsonify({
                "result": {
                    "img": served_img_url
                }
            })
        else:
            return jsonify({"status": 500, "error": "Failed to download the generated image."}), 500
    else:
        return jsonify({"status": 500, "error": "Failed to generate the anime image."}), 500

if __name__ == "__main__":
    app.run(debug=True)
