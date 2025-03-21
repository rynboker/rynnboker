from flask import Flask, jsonify, request
import requests
import logging
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

        # Konfigurasi API Weather
@app.route('/api/wmit', methods=['GET'])
def wmit():
    img = request.args.get('img')
    if not img:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'img' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/wmit?apikey=youga&img={img}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

              # Konfigurasi API Weather
@app.route('/api/wait', methods=['GET'])
def wait():
    img = request.args.get('img')
    if not img:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'img' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/wait?apikey=youga&img={img}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

        # Konfigurasi API Weather
@app.route('/api/nhentai', methods=['GET'])
def nhentai():
    code = request.args.get('code')
    if not code:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'code' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/nhentai/{code}?apikey=youga"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

        # Konfigurasi API Weather
@app.route('/api/nhentaisearch', methods=['GET'])
def nhentaisearch():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/nhentaisearch?apikey=youga&query={message}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

        # Konfigurasi API Weather
@app.route('/api/gimage2', methods=['GET'])
def gimage2():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/gimage2?apikey=youga&query={message}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

                # Konfigurasi API Weather
@app.route('/api/ouobypass', methods=['GET'])
def ouobypass():
    link = request.args.get('link')
    if not link:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'link' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/ouo?apikey=youga&url={link}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

                # Konfigurasi API Weather
@app.route('/api/tiktokmusic', methods=['GET'])
def tiktokmusic():
    link = request.args.get('link')
    if not link:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'link' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/tiktokmusic?apikey=youga&url={link}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

 # Konfigurasi API Weather
@app.route('/api/tiktoknowm', methods=['GET'])
def tiktoknowm():
    link = request.args.get('link')
    if not link:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'link' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/tiktok2?apikey=youga&url={link}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

 # Konfigurasi API Weather
@app.route('/api/telestick', methods=['GET'])
def telestick():
    link = request.args.get('link')
    if not link:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'link' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/telestick?apikey=youga&url={link}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

 # Konfigurasi API Weather
@app.route('/api/growikibeta', methods=['GET'])
def growikibeta():
    item = request.args.get('item')
    if not item:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'item' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/growiki?apikey=youga&query={item}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "result" not in external_data or not external_data["result"]:
            return jsonify({
                "status": 502,
                "creator": "NoMeL",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "NoMeL",
            "data": external_data["result"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "NoMeL",
            "error": f"Service is unavailable"
        }), 503

# API untuk mengambil data dari halaman Growtopia
@app.route('/api/growtopia', methods=['GET'])
def growtopia():
    # Parameter untuk menentukan URL atau informasi tambahan lainnya
    url = request.args.get('url', 'https://www.growtopiagame.com/detail')
    
    # Ambil halaman HTML dari URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503
    
    # Parsing halaman HTML dengan BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ambil jumlah online_user (Contoh selector, sesuaikan dengan elemen HTML yang sebenarnya)
    online_user = soup.find('div', class_='online-user')  # Pastikan selector sesuai
    online_user_count = online_user.text.strip() if online_user else "Unknown"

    # Ambil full_size gambar (Contoh selector, sesuaikan dengan elemen HTML yang sebenarnya)
    world_day_images = soup.find('img', class_='world-image')  # Pastikan selector sesuai
    full_size = world_day_images['src'] if world_day_images else "Unknown"

    # Mengubah logika di sini: parse online_user dan full_size gambar sesuai permintaan kamu
    playerCount = int(online_user_count) if online_user_count.isdigit() else 0
    wotdURL = full_size

    # Kembalikan data dalam format JSON
    return jsonify({
        "status": 200,
        "creator": "Astri",
        "data": {
            "player_count": playerCount,
            "world_of_the_day_image": wotdURL
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
