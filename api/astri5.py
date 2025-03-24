from flask import Flask, jsonify, request
import requests
import logging
from datetime import datetime

app = Flask(__name__)

# Konfigurasi API Weather
@app.route('/api/weather', methods=['GET'])
def weather():
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
            "error": f"Service is unavailable"
        }), 503

        # Konfigurasi API Weather
@app.route('/api/corona/indonesia', methods=['GET'])
def coronaindonesia():

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/corona/indonesia?apikey=youga"
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
@app.route('/api/corona/global', methods=['GET'])
def coronaglobal():

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/corona/global?apikey=youga"
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
@app.route('/api/minecraft', methods=['GET'])
def minecraft():
    serverurl = request.args.get('serverurl')
    if not serverurl:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'serverurl' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/minecraft/{serverurl}?apikey=youga"
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
@app.route('/api/ppcouple', methods=['GET'])
def ppcouple():

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/random/ppcouple?apikey=youga"
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
@app.route('/api/ytchannel', methods=['GET'])
def ytchannel():
    channel = request.args.get('channel')
    if not channel:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'channel' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.lolhuman.xyz/api/ytchannel?apikey=youga&query={channel}"
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

if __name__ == "__main__":
    app.run(debug=True)
