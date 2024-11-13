from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/idk/otakulatest', methods=['GET'])
def otakulatest():

    # Panggil API eksternal untuk mencari video di YouTube
    api_url = f"https://api.agatz.xyz/api/otakulatest"
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

        # Menangani kategori on_going dan complete
        results_on_going = []
        results_complete = []
        
        # Proses kategori on_going
        for item in data.get("data", {}).get("home", {}).get("on_going", []):
            results_on_going.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "day_updated": item.get("day_updated"),
                "link": item.get("link")
            })

        # Proses kategori complete
        for item in data.get("data", {}).get("home", {}).get("complete", []):
            results_complete.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "score": item.get("score"),
                "link": item.get("link")
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "on_going": results_on_going,
            "complete": results_complete
        })

    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred")
        return jsonify({
            "status": 503,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "error": "Service is unavailable. Please try again later."
        }), 503
