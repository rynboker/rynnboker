import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/gempa', methods=['GET'])
def gempa():

    # Call the external earthquake data API
    api_url = f"https://api.agatz.xyz/api/gempa"
    try:
        response = requests.get(api_url)

        # Handle any non-200 responses from the external API
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        # Extract and format the data from the external API response
        external_data = response.json().get("data", {})

        # Check if external data is present
        if not external_data:
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No earthquake data found."
            }), 404

        # Format the data as needed
        formatted_data = {
            "date": external_data.get("tanggal"),
            "time": external_data.get("waktu"),
            "potential": external_data.get("potensi"),
            "magnitude": external_data.get("magnitude"),
            "depth": external_data.get("kedalaman"),
            "region": external_data.get("wilayah"),
            "latitude": external_data.get("lintang"),
            "longitude": external_data.get("bujur"),
            "coordinates": external_data.get("koordinat"),
            "felt": external_data.get("dirasakan")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": "An unexpected error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
