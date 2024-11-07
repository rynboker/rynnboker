from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/gptlogic', methods=['GET'])
def my_api():
    try:
        # Ambil parameter dari request
        logic = request.args.get('logic')
        p = request.args.get('p')

        # Validasi parameter
        if not logic or not p:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Parameters 'logic' and 'p' are required."
            }), 400

        # Panggil API eksternal
        api_url = f"https://api.agatz.xyz/api/gptlogic?logic={logic}&p={p}"
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
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": data.get("data")
        })

    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred: {str(e)}")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

    except Exception as e:
        # Tangani error tak terduga lainnya
        print(f"Unexpected error: {str(e)}")
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": "An error occurred on our server."
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
