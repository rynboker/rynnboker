import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/spotify', methods=['GET'])
def spotify():
    try:
        # Get the 'message' parameter for the YouTube search query
        message = request.args.get('message')

        if not message:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Missing parameter 'message'."
            }), 400

        # Call the external YouTube search API
        api_url = f"https://api.agatz.xyz/api/spotify?message={message}"
        response = requests.get(api_url)

        # If external API request failed
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "External API failed."
            }), response.status_code

        # Return the YouTube search results
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": response.data.data
        })

    except requests.exceptions.RequestException as e:
        # Handle network or server errors
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"External API request failed: {e}"
        }), 503

    except Exception as e:
        # Handle other unexpected errors
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
