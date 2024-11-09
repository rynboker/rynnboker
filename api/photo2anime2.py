import os
import requests
from flask import Flask, request, jsonify
from io import BytesIO
from pathlib import Path
from PIL import Image

app = Flask(__name__)

# Folder publik untuk menyimpan gambar
PUBLIC_IMAGE_DIR = Path(__file__).parent / 'public'

# Pastikan folder publik ada
PUBLIC_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Mendapatkan URL gambar dari parameter query
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({"creator": "Astri", "error": "URL parameter is missing.", "status": 400})

    try:
        # Mengambil gambar dari URL
        response = requests.get(image_url)

        if response.status_code != 200:
            return jsonify({"creator": "Astri", "error": "Failed to retrieve the image.", "status": 500})

        # Membuka gambar dari konten respons
        img = Image.open(BytesIO(response.content))

        # Tentukan path file gambar di folder publik
        filename = os.path.basename(image_url)
        file_path = PUBLIC_IMAGE_DIR / filename

        # Menyimpan gambar ke folder publik
        img.save(file_path)

        # URL gambar yang dapat diakses secara publik
        served_img_url = f"https://www.youga.my.id/images/{filename}"

        # Mengembalikan URL gambar dalam response
        return jsonify({
            "creator": "Astri",
            "status": 200,
            "image_url": served_img_url
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": 500})

if __name__ == '__main__':
    app.run(debug=True)
