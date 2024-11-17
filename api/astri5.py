from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# API for weather
@app.route('/api/weather', methods=['GET'])
def weather():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/cuaca?message={message}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise error if status code is 4xx or 5xx

        # Forward the entire response JSON
        data = response.json()
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": data
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "status": 504,
            "creator": "Astri",
            "error": "The request to the external service timed out. Please try again later."
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable: {str(e)}"
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
