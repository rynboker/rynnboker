import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/ytplayvid', methods=['GET'])
def ytplayvid():
    try:
        # Get parameters from the request
        message = request.args.get('message')

    # Validasi parameter
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

        # Call the external API
        api_url = f"https://api.agatz.xyz/api/ytplayvid?message={message}"

        # If external API request failed
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
                "title": item.get("title"),
                "description": item.get("description"),
                "url": item.get("url"),
                "duration": item.get("duration"),
                "views": item.get("views"),
                "uploadedAt": item.get("uploadedAt"),
                "author": item.get("author"),
                "downloadUrl": item.get("downloadUrl")
            })
        
        return jsonify({
            "status": 200,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "data": results
        })
    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred: {str(e)}")
        return jsonify({
            "status": 503,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "error": "Service is unavailable. Please try again later."
        }), 503

if __name__ == '__main__':
    app.run(debug=True)
