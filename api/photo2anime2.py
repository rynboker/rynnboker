import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from io import BytesIO
from pathlib import Path
from PIL import Image

app = Flask(__name__)

# Use /tmp directory on Vercel for storing images (Writable directory)
PUBLIC_IMAGE_DIR = '/tmp'

# Ensure the temporary directory exists
Path(PUBLIC_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

# Helper function to call the external API
def transform_image(image_url, version_type):
    api_url = "https://itzpire.com/tools/photo2anime2"
    params = {
        "url": image_url,
        "type": version_type
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code != 200:
        return None
    
    result = response.json()
    if "result" in result:
        return result["result"]
    else:
        return None

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Get the image URL and type from the request
    image_url = request.args.get('url')
    version_type = request.args.get('type', 'version 0.2')  # Default to version 0.2
    
    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    # Validate version type
    if version_type not in ['version 0.2', 'version 0.3', 'version 0.4']:
        return jsonify({"creator": "Astri", "error": "Invalid version type.", "status": 400})
    
    try:
        # Call the external API to transform the image
        anime_image_url = transform_image(image_url, version_type)

        if not anime_image_url:
            return jsonify({"creator": "Astri", "error": "Failed to transform the image.", "status": 500})

        # Save the transformed image to /tmp directory
        response = requests.get(anime_image_url)
        if response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to retrieve transformed image.", "status": 500})

        # Open the image from the response content
        img = Image.open(BytesIO(response.content))

        # Define a temporary image file path
        img_name = os.path.basename(anime_image_url)
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        # Save the image to the temporary directory
        img.save(img_path)

        # Construct the served image URL based on your domain
        served_img_url = f"https://www.youga.my.id/api/photo2anime2_image/{img_name}"

        # Check if the image was saved successfully
        if not os.path.exists(img_path):
            return jsonify({"creator": "Astri", "error": "Image was not saved.", "status": 500})

        # Return the image URL in the response
        return jsonify({
            "creator": "Astri",
            "status": 200,
            "image_url": served_img_url
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": 500})

@app.route('/api/photo2anime2_image/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        # Define the image path in the tmp directory
        image_path = os.path.join(PUBLIC_IMAGE_DIR, filename)
        
        # Check if the file exists, and if it does, serve it
        if os.path.exists(image_path):
            return send_from_directory(PUBLIC_IMAGE_DIR, filename)
        else:
            return jsonify({"error": "File not found", "status": 404})

    except Exception as e:
        return jsonify({"error": str(e), "status": 500})

if __name__ == '__main__':
    app.run(debug=True)
                        
