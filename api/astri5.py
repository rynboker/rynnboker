from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/cuaca', methods=['GET'])
def cuaca():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.agatz.xyz/api/cuaca?message={message}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()  # Data dari API agatz

        # Validasi apakah respons berisi data yang diharapkan
        if "data" not in external_data or not external_data["data"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["data"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable: {str(e)}"
        }), 503


if __name__ == "__main__":
    app.run(debug=True)
