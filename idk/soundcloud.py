from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/idk/soundcloud', methods=['GET'])
def soundcloud():
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
    api_url = f"https://api.agatz.xyz/api/soundcloud?message={message}"
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
            results.append({
                "link": item.get("link"),
                "title": item.get("judul")
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
