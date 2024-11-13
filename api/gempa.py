import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/gempa', methods=['GET'])
def gempa():
    # Call the external earthquake data API
    api_url1 = f"https://api.agatz.xyz/api/gempa"
    api_url2 = f"https://itzpire.com/information/gempaWarning"

    try:
        # Make the API requests
        response1 = requests.get(api_url1)
        response2 = requests.get(api_url2)

        # Handle any non-200 responses from the external API
        if response1.status_code != 200:
            return jsonify({
                "status": response1.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response1.status_code

        if response2.status_code != 200:
            return jsonify({
                "status": response2.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response2.status_code

        # Extract and format the data from the external API response
        external_data1 = response1.json().get("data", {})
        external_data2 = response2.json().get("data", {})

        # Check if external data is present
        if not external_data1:
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No earthquake data found."
            }), 404

        if not external_data2:
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No earthquake data found."
            }), 404

        # Format the data as needed
        formatted_data1 = {
            "date": external_data1.get("tanggal"),
            "time": external_data1.get("waktu"),
            "potential": external_data1.get("potensi"),
            "magnitude": external_data1.get("magnitude"),
            "depth": external_data1.get("kedalaman"),
            "region": external_data1.get("wilayah"),
            "latitude": external_data1.get("lintang"),
            "longitude": external_data1.get("bujur"),
            "coordinates": external_data1.get("koordinat"),
            "felt": external_data1.get("dirasakan")
        }

        formatted_data2 = {
            "peta": external_data2.get("linkPeta")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data1": formatted_data1,
            "data2": formatted_data2
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
