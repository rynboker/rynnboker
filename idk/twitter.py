import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/idk/twitter', methods=['GET'])
def twitter():
    url = request.args.get('url')

    # Validate the required parameter
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    # Call the external image search API
    api_url = f"https://api.agatz.xyz/api/twitter?url={url}"
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
                "desc": item.get("desc"),
                "thumb": item.get("thumb"),
                "video_sd": item.get("video_sd"),
                "video_hd": item.get("video_hd"),
                "audio": item.get("audio")
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
