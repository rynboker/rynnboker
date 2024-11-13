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

# ImgBB API Key
IMGBB_API_KEY = '366a731c8d1387832871de9b04a6a0f4'  # Masukkan API Key ImgBB Anda di sini

# Ensure the temporary directory exists
Path(PUBLIC_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

# /api/photo2anime2 Endpoint
@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    image_url = request.args.get('url')
    type_version = request.args.get('type', '2')  # Default to '2' if no type is specified

    # Validate type_version
    if type_version not in ['2', '3', '4']:
        return jsonify({"creator": "Astri", "error": "Invalid type parameter. Valid values are 2, 3, 4.", "status": 400})

    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    try:
        # Request image from the provided URL
        img_response = requests.get(image_url)
        if img_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to download image from the provided URL.", "status": 500})

        # Upload the image to ImgBB
        imgbb_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}&expiration=300"
        imgbb_response = requests.post(imgbb_url, files={"image": img_response.content})
        
        if imgbb_response.status_code != 200:
            return jsonify({
                "creator": "Astri", 
                "error": f"Failed to upload the image to ImgBB. Response: {imgbb_response.json()}",
                "status": 500
            })
        
        # Get the ImgBB image URL from the response
        imgbb_data = imgbb_response.json()
        if "data" in imgbb_data and "url" in imgbb_data["data"]:
            imgbb_img_url = imgbb_data["data"]["url"]
        else:
            return jsonify({"creator": "Astri", "error": "Invalid response from ImgBB.", "status": 500})

        # Now use the image URL from ImgBB to call the photo2anime API
        api_url = f"https://itzpire.com/tools/photo2anime2?url={imgbb_img_url}&type=version%200.{type_version}"
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200 and "result" in data and "img" in data["result"]:
            anime_img_url = data['result']['img']
            duration = data['result'].get('duration', 0)
        else:
            return jsonify({"creator": "Astri", "error": "Invalid API response format.", "status": 500})

        # Save the transformed image to the temporary directory
        img_name = os.path.basename(anime_img_url)
        img_name = img_name.split('?')[0]  # Clean the filename in case the URL has query params
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        # Fetch the image from the anime image URL and save it
        img_response = requests.get(anime_img_url)
        if img_response.status_code == 200:
            img = Image.open(BytesIO(img_response.content))
            img.save(img_path)
        else:
            return jsonify({"creator": "Astri", "error": "Failed to fetch the generated image.", "status": 500})

        # Construct the served image URL based on your domain
        served_img_url = f"https://www.youga.my.id/api/photo2anime2_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "original_image_url": imgbb_img_url,
            "anime_image_url": served_img_url,
            "duration": duration,
            "type_version": type_version
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "creator": "Astri", 
            "error": "The API request timed out. Please try again later.", 
            "status": 504
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "creator": "Astri", 
            "error": "Error with the API request.", 
            "status": 500
        })
    except ValueError:
        return jsonify({
            "creator": "Astri", 
            "error": "Received invalid JSON from the API.", 
            "status": 500
        })
    except Exception as e:
        return jsonify({
            "creator": "Astri", 
            "error": f"Unexpected error occurred", 
            "status": 500
        })

# Endpoint to serve the image from the temporary directory
@app.route('/api/photo2anime2_image/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        image_path = os.path.join(PUBLIC_IMAGE_DIR, filename)
        
        if os.path.exists(image_path):
            return send_from_directory(PUBLIC_IMAGE_DIR, filename)
        else:
            return jsonify({
                "error": "File not found", 
                "status": 404
            })

    except Exception as e:
        return jsonify({
            "error": f"500 - Something went wrong", 
            "status": 500
        })

# /api/gempa Endpoint
@app.route('/api/gempa', methods=['GET'])
def gempa():
    api_url = f"https://api.agatz.xyz/api/gempa"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "date": item.get("tanggal"),
                "time": item.get("waktu"),
                "potential": item.get("potensi"),
                "magnitude": item.get("magnitude"),
                "depth": item.get("kedalaman"),
                "region": item.get("wilayah"),
                "latitude": item.get("lintang"),
                "oblong": item.get("bujur"),
                "coordinate": item.get("koordinat"),
                "felt": item.get("dirasakan")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

# /api/gimage Endpoint
@app.route('/api/gimage', methods=['GET'])
def gimage():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/gimage?message={message}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "url": item.get("url"),
                "height": item.get("height"),
                "width": item.get("width")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

# /api/gptlogic Endpoint
@app.route('/api/gptlogic', methods=['GET'])
def gptlogic():
    try:
        logic = request.args.get('logic')
        p = request.args.get('p')

        if not logic or not p:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Missing parameters 'logic' or 'p'."
            }), 400

        api_url = f"https://api.agatz.xyz/api/gptlogic?logic={logic}&p={p}"
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "External API failed."
            }), response.status_code

        data = response.json()
        result = data.get("data", {}).get("result", "No result found.")

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": {
                "result": result
            }
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"External API request failed"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

# /api/pinterest Endpoint
@app.route('/api/pinterest', methods=['GET'])
def pinterest():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/pinsearch?message={message}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "pin": item.get("pin"),
                "created_at": item.get("created_at"),
                "id": item.get("id"),
                "images_url": item.get("images_url"),
                "grid_title": item.get("grid_title")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)