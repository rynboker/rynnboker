import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/ytplayvid', methods=['GET'])
def ytplayvid():
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
        api_url = f"https://api.agatz.xyz/api/ytplayvid?message={message}"
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

        # Format the response data as desired
        results = []
        for item in data.get("data", []):
            results.append({
                "title": item.get("title"),
                "description": item.get("description"),
                "url": item.get("url"),
                "duration": item.get("duration"),
                "views": item.get("views"),
                "uploadedAt": item.get("uploadedAt"),
                "author": item.get("author"),
                "downloadUrl": item.get("downloadUrl")
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })

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
