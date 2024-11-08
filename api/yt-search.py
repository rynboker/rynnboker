import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/ytsearch', methods=['GET'])
def ytsearch():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # Call external YouTube search API
    api_url = f"https://api.agatz.xyz/api/ytsearch?message={message}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": data.get("data")
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable: {str(e)}"
        }), 503
    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
