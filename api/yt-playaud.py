import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/ytplayaud', methods=['GET'])
def ytplayaud():
    try:
        # Get parameters from the request
        message = request.args.get('message')

        # Validate the parameter
        if not message:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Parameter 'message' is required."
            }), 400

        # Call the external API
        api_url = f"https://api.agatz.xyz/api/ytplayaud?message={message}"
        response = requests.get(api_url)

        # Check if the external API request was successful
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        # Get data from the external API response
        data = response.json()

        # Extract information according to the provided JSON structure
        info = data.get("data", {}).get("info", {})
        audio = data.get("data", {}).get("audio", {})

        # Format the response data as desired
        result = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "success": data.get("data", {}).get("success", False),
                "info": {
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "views": info.get("views"),
                    "author": {
                        "name": info.get("author", {}).get("name"),
                        "url": info.get("author", {}).get("url")
                    },
                    "thumbnail": info.get("thumbnail"),
                    "uploaded": info.get("uploaded"),
                    "duration": info.get("duration"),
                    "url": info.get("url")
                },
                "audio": {
                    "size": audio.get("size"),
                    "format": audio.get("format"),
                    "url": audio.get("url")
                }
            }
        }

        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        # Handle network or server errors
        print(f"Error occurred: {str(e)}")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

if __name__ == '__main__':
    app.run(debug=True)
