import os
import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pathlib import Path
from PIL import Image
import tempfile

app = Flask(__name__)

# Public directory for serving images
PUBLIC_IMAGE_DIR = './tmp/temp_images'

# Ensure the public directory exists
Path(PUBLIC_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Get the image URL from the request
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    try:
        # Fetch the image from the URL
        response = requests.get(image_url)

        if response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to retrieve the image.", "status": 500})

        # Open the image from the response content
        img = Image.open(BytesIO(response.content))

        # Define a public image file path
        img_name = os.path.basename(image_url)
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        # Save the image to the public directory
        img.save(img_path)

        # Construct the served image URL based on your domain
        served_img_url = f"https://www.youga.my.id/tmp/{img_name}"

        # Return the image URL in the response
        return jsonify({
            "creator": "Astri",
            "status": 200,
            "image_url": served_img_url
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": 500})

if __name__ == '__main__':
    app.run(debug=True)
