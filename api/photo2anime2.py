import os
import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pathlib import Path
from PIL import Image

app = Flask(__name__)

IMGBB_API_KEY = '366a731c8d1387832871de9b04a6a0f4'  # API Key untuk imgbb

# Endpoint untuk menerima URL dan mengonversi gambar
@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Mendapatkan URL gambar dari request dan tipe konversi
    image_url = request.args.get('url')
    type_version = request.args.get('type', '2')  # Default ke '2' jika tidak ditentukan
    
    # Validasi tipe versi untuk memastikan hanya nilai tertentu yang diterima
    if type_version not in ['2', '3', '4']:
        return jsonify({"creator": "Astri", "error": "Invalid type parameter. Valid values are 2, 3, 4.", "status": 400})

    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    try:
        # Unggah gambar ke imgbb dari URL awal
        imgbb_url = f"https://api.imgbb.com/1/upload?expiration=300&key={IMGBB_API_KEY}"
        imgbb_response = requests.post(imgbb_url, data={"image": image_url})
        
        if imgbb_response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to upload the image to imgbb.", "status": 500})

        imgbb_data = imgbb_response.json()
        if "data" in imgbb_data and "url" in imgbb_data["data"]:
            imgbb_img_url = imgbb_data["data"]["url"]
        else:
            return jsonify({"creator": "Astri", "error": "Invalid response from imgbb.", "status": 500})

        # Gunakan URL dari imgbb sebagai input untuk API photo2anime2
        api_url = f"https://itzpire.com/tools/photo2anime2?url={imgbb_img_url}&type=version%200.{type_version}"
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse respons untuk mendapatkan URL gambar yang dihasilkan
        data = response.json()
        if data.get("code") == 200 and "result" in data and "img" in data["result"]:
            anime_img_url = data['result']['img']
            duration = data['result'].get('duration', 0)  # Durasi default 0 jika tidak ada
        else:
            return jsonify({"creator": "Astri", "error": "Invalid API response format.", "status": 500})

        # Kembalikan URL gambar hasil dari photo2anime2
        return jsonify({
            "creator": "Astri",
            "status": 200,
            "original_image_url": imgbb_img_url,  # URL gambar di imgbb
            "anime_image_url": anime_img_url,  # URL gambar hasil konversi
            "duration": duration,  # Sertakan durasi di respons
            "type_version": type_version  # Sertakan tipe versi yang digunakan
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
            "error": f"Error with the API request", 
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

if __name__ == '__main__':
    app.run(debug=True)
