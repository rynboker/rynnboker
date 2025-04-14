import os
from flask import Flask, jsonify, send_from_directory, request
import requests
from pathlib import Path

app = Flask(__name__)

# Use /tmp directory on Vercel for storing images (Writable directory)
PUBLIC_IMAGE_DIR = '/tmp'

# ImgBB API Key
IMGBB_API_KEY = '366a731c8d1387832871de9b04a6a0f4'  # Masukkan API Key ImgBB Anda di sini

# Ensure the temporary directory exists
Path(PUBLIC_IMAGE_DIR).mkdir(parents=True, exist_ok=True)

# /api/random_neko Endpoint
@app.route('/api/random_neko', methods=['GET'])
def random_neko():
    try:
        # Request image directly from the Lolhuman API
        lolhuman_url = "https://api.lolhuman.xyz/api/random/sfw/neko?apikey=59485720964df592a349c173"
        lolhuman_response = requests.get(lolhuman_url, stream=True)
        
        if lolhuman_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch image.", "status": 500})

        # Save the image locally to the temporary directory
        img_name = "neko_image.jpg"  # A default filename
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        with open(img_path, 'wb') as file:
            for chunk in lolhuman_response.iter_content(1024):
                file.write(chunk)

        # Upload the saved image to ImgBB
        with open(img_path, 'rb') as img_file:
            imgbb_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}&expiration=300"
            imgbb_response = requests.post(imgbb_url, files={"image": img_file})
        
        if imgbb_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to upload image to ImgBB.", "status": 500})

        # Get the ImgBB image URL from the response
        imgbb_data = imgbb_response.json()
        if "data" in imgbb_data and "url" in imgbb_data["data"]:
            imgbb_img_url = imgbb_data["data"]["url"]
        else:
            return jsonify({"creator": "Astri", "error": "Invalid response from ImgBB.", "status": 500})

        # Construct the served image URL
        served_img_url = f"https://www.youga.my.id/api/random_neko_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "uploaded_image_url": imgbb_img_url,
            "served_image_url": served_img_url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": "Error with API request.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": f"Unexpected error occurred", "status": 500})

# /api/removebg Endpoint
@app.route('/api/removebg', methods=['GET'])
def removebg():
    image_url = request.args.get('img')
    if not image_url:
        return jsonify({"creator": "Astri", "error": "Missing 'img' parameter.", "status": 400})

    try:
        # Request image from the removebg API
        removebg_url = f"https://api.lolhuman.xyz/api/removebg?apikey=59485720964df592a349c173&img={image_url}"
        removebg_response = requests.get(removebg_url, stream=True)
        
        if removebg_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch image from removebg API.", "status": 500})

        # Save the image locally
        img_name = "removebg_image.png"
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        with open(img_path, 'wb') as file:
            for chunk in removebg_response.iter_content(1024):
                file.write(chunk)

        served_img_url = f"https://www.youga.my.id/api/removebg_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "served_image_url": served_img_url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": "Error with API request.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": f"Unexpected error occurred", "status": 500})

# /api/upscale Endpoint
@app.route('/api/upscale', methods=['GET'])
def upscale():
    image_url = request.args.get('img')
    if not image_url:
        return jsonify({"creator": "Astri", "error": "Missing 'img' parameter.", "status": 400})

    try:
        # Request image from the upscale API
        upscale_url = f"https://api.lolhuman.xyz/api/upscale?apikey=59485720964df592a349c173&img={image_url}"
        upscale_response = requests.get(upscale_url, stream=True)
        
        if upscale_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch image from upscale API.", "status": 500})

        # Save the image locally
        img_name = "upscale_image.png"
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        with open(img_path, 'wb') as file:
            for chunk in upscale_response.iter_content(1024):
                file.write(chunk)

        served_img_url = f"https://www.youga.my.id/api/upscale_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "served_image_url": served_img_url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": "Error with API request.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": f"Unexpected error occurred", "status": 500})

# /api/bubblechat Endpoint
@app.route('/api/bubblechat', methods=['GET'])
def bubblechat():
    avatar_url = request.args.get('avatar')
    name = request.args.get('name')
    text = request.args.get('text')

    if not avatar_url or not name or not text:
        return jsonify({"creator": "Astri", "error": "Missing required parameters: 'avatar', 'name', 'text'.", "status": 400})

    try:
        # Request image from the bubblechat API
        bubblechat_url = f"https://api.lolhuman.xyz/api/bubblechat?apikey=59485720964df592a349c173&avatar={avatar_url}&name={name}&text={text}"
        bubblechat_response = requests.get(bubblechat_url, stream=True)
        
        if bubblechat_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch image from bubblechat API.", "status": 500})

        # Save the image locally
        img_name = "bubblechat_image.png"
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        with open(img_path, 'wb') as file:
            for chunk in bubblechat_response.iter_content(1024):
                file.write(chunk)

        served_img_url = f"https://www.youga.my.id/api/bubblechat_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "served_image_url": served_img_url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": "Error with API request.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": f"Unexpected error occurred", "status": 500})

# /api/nulis Endpoint
@app.route('/api/nulis', methods=['GET'])
def nulis():
    text = request.args.get('text')
    if not text:
        return jsonify({"creator": "Astri", "error": "Missing 'text' parameter.", "status": 400})

    try:
        # Request image from the nulis API
        nulis_url = f"https://api.lolhuman.xyz/api/nulis?apikey=59485720964df592a349c173&text={text}"
        nulis_response = requests.get(nulis_url, stream=True)
        
        if nulis_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to fetch image from nulis API.", "status": 500})

        # Save the image locally
        img_name = "nulis_image.png"
        img_path = os.path.join(PUBLIC_IMAGE_DIR, img_name)

        with open(img_path, 'wb') as file:
            for chunk in nulis_response.iter_content(1024):
                file.write(chunk)

        served_img_url = f"https://www.youga.my.id/api/nulis_image/{img_name}"

        return jsonify({
            "creator": "Astri",
            "status": 200,
            "served_image_url": served_img_url
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"creator": "Astri", "error": "Error with API request.", "status": 500})
    except Exception as e:
        return jsonify({"creator": "Astri", "error": f"Unexpected error occurred", "status": 500})

# Serve the image from the temporary directory
@app.route('/api/removebg_image/<filename>', methods=['GET'])
def serve_image(filename):
    try:
        image_path = os.path.join(PUBLIC_IMAGE_DIR, filename)
        if os.path.exists(image_path):
            return send_from_directory(PUBLIC_IMAGE_DIR, filename)
        else:
            return jsonify({"error": "File not found", "status": 404}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error occurred", "status": 500}), 500


if __name__ == '__main__':
    app.run(debug=True)
