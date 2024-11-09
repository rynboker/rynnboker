import os
import random
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

# Endpoint to accept the URL and type for the transformation
@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Get the image URL and type from the request
    image_url = request.args.get('url')
    type_version = request.args.get('type', '2')  # Default to '2' if no type is specified
    
    # Validate type_version to ensure it's one of the supported values
    if type_version not in ['2', '3', '4']:
        return jsonify({"creator": "Astri", "error": "Invalid type parameter. Valid values are 2, 3, 4.", "status": 400})

    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    try:
        # Make a request to the  API to get the image
        api_url = f"https://itzpire.com/tools/photo2anime2?url={image_url}&type=version%200.{type_version}"
        response = requests.get(api_url, timeout=20)  # Adjust timeout as needed
        response.raise_for_status()  # Raise an error for any HTTP issues

        # Parse the response to extract the image URL and duration
        data = response.json()
        if data.get("code") == 200 and "result" in data and "img" in data["result"]:
            img_url = data['result']['img']
            duration = data['result'].get('duration', 0)  # Default duration to 0 if missing
        else:
            return jsonify({"creator": "Astri", "error": "Invalid API response format.", "status": 500})

        # Fetch the image from the  URL
        img_response = requests.get(img_url)
        if img_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch the generated image.", "status": 500})

        # Open the image from the response content
        img = Image.open(BytesIO(img_response.content))

        # Define a temporary image file path
        img_name = os.path.basename(img_url)
        img_name = img_name.split('?')[0]  # Clean the filename in case the URL has query params
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        # Save the image to the temporary directory
        img.save(img_path)

        # Construct the served image URL based on your domain
        served_img_url = f"https://www.youga.my.id/api/photo2anime2_image/{img_name}"

        # Check if the image was saved successfully
        if not os.path.exists(img_path):
            return jsonify({"creator": "Astri", "error": "Image was not saved.", "status": 500})

        # Return the image URL, duration, and other info in the response
        return jsonify({
            "creator": "Astri",
            "status": 200,
            "image_url": served_img_url,
            "duration": duration,  # Include the duration in the response
            "type_version": type_version  # Include the type/version used in the request
        })

    except requests.exceptions.Timeout:
        return jsonify({"creator": "Astri", "error": "The  API request timed out. Please try again later.", "status": 504})
    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": f"Error with the API request", "status": 500})
    except ValueError:
        return jsonify({"creator": "Astri", "error": "Received invalid JSON from the API.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": "An unexpected error occurred. Please try again later.", "status": 500})

# Endpoint to serve the image from the temporary directory
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
        return jsonify({"error": f"500 - Something went wrong", "status": 500})

if __name__ == '__main__':
    app.run(debug=True)
