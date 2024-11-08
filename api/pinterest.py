import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/pinterest', methods=['GET'])
def pinterest():
    message = request.args.get('message')

    # Validate the required parameter
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # Call the external image search API
    api_url = f"https://api.agatz.xyz/api/pinterest?message={message}"
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
                "pin": item.get("pin"),
                "created_at": item.get("created_at"),
                "id": item.get("id"),
                "images_url": item.get("images_url"),
                "grid_title": item.get("grid_title")
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
