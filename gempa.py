import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/gempa', methods=['GET'])
def gempa():

    # Call the external image search API
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

        # Extract and format the data as needed
        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "date": item.get("tanggal"),
                "time": item.get("waktu"),
                "potential": item.get("potensi"),
                "magnitude": item.get("magnitude"),
                "depth": item.get("kedalaman"),
                "region": item.get("wilayah"),
                "latitude": item.get("lintang"),
                "oblong": item.get("bujur"),
                "coordinate": item.get("koordinat"),
                "felt": item.get("dirasakan")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
