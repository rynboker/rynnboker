from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/otakudesu', methods=['GET'])
def otakudesu():
    # Ambil parameter message dari request
    message = request.args.get('message')

    # Validasi parameter
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # Panggil API eksternal untuk mencari video di YouTube
    api_url = f"https://api.agatz.xyz/api/otakudesu?message={message}"
    try:
        response = requests.get(api_url)
        # Jika respons dari API eksternal tidak berhasil
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        # Ambil data dari respons API eksternal
        data = response.json()

        # Buat respons sesuai dengan format yang diinginkan
       results = []
        for item in data.get("data", []):
            # Ambil genre yang bisa lebih dari satu
            genre_list = item.get("genre_list", [])
            
            # Jika genre_list ada dan bukan kosong, buat list of genres
            genres = []
            for genre in genre_list:
                genres.append({
                    "genre_title": genre.get("genre_title"),
                    "genre_link": genre.get("genre_link"),
                    "genre_id": genre.get("genre_id")
                })
            
            # Jika genre tidak ditemukan, kirim nilai default kosong
            if not genres:
                genres = None

            results.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "link": item.get("link"),
                "id": item.get("id"),
                "status": item.get("status"),
                "score": item.get("score"),
                "genre": genres  # Memasukkan daftar genre
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "data": results
        })
    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred")
        return jsonify({
            "status": 503,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "error": "Service is unavailable. Please try again later."
        }), 503
