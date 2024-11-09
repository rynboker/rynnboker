import os
import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pathlib import Path
from PIL import Image
import tempfile

app = Flask(__name__)

# Temporary directory for saving the images
TEMP_IMAGE_DIR = '/tmp/temp_images'

# Ensure the temporary directory exists
Path(TEMP_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
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

        # Define a temporary image file path in the writable /tmp directory
        with tempfile.NamedTemporaryFile(delete=False, dir=TEMP_IMAGE_DIR, suffix=".png") as temp_img_file:
            temp_img_path = temp_img_file.name

        # Save the image to the temporary file
        img.save(temp_img_path)

        # Construct the served image URL based on your domain
        served_img_url = f"https://www.youga.my.id/tmp/{os.path.basename(temp_img_path)}"

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
