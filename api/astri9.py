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
        response.raise_for_status()  # Raises an HTTPError if the status code is 4xx/5xx
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable. Error: {str(e)}"
        }), 503
    
    # Parsing halaman HTML dengan BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ambil jumlah online_user (Pastikan selector sesuai dengan elemen HTML yang benar)
    online_user = soup.find('div', class_='online-user')  # Ganti dengan selector yang benar
    if online_user:
        online_user_count = online_user.text.strip()
    else:
        return jsonify({
            "status": 404,
            "creator": "Astri",
            "error": "Could not find the online user element on the page."
        }), 404
    
    # Ambil full_size gambar (Pastikan selector sesuai dengan elemen HTML yang benar)
    world_day_images = soup.find('img', class_='world-image')  # Ganti dengan selector yang benar
    if world_day_images and 'src' in world_day_images.attrs:
        full_size = world_day_images['src']
    else:
        return jsonify({
            "status": 404,
            "creator": "Astri",
            "error": "Could not find the world of the day image on the page."
        }), 404

    # Mengubah logika di sini: parse online_user dan full_size gambar sesuai permintaan kamu
    player_count = int(online_user_count) if online_user_count.isdigit() else 0
    wotd_url = full_size

    # Kembalikan data dalam format JSON
    return jsonify({
        "status": 200,
        "creator": "Astri",
        "data": {
            "player_count": player_count,
            "world_of_the_day_image": wotd_url
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
