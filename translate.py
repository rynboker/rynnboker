import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/translate', methods=['GET'])
def translate_text():
    # Get the 'text' and 'to' parameters from the request
    text = request.args.get('text')
    to_language = request.args.get('to', 'en')  # Default to 'en' if 'to' is not provided

    if not text:
        return jsonify({
            "status": 400,
            "error": "Parameter 'text' is required."
        }), 400

    # Call the Popcat API
    popcat_url = "https://api.popcat.xyz/translate"
    try:
        response = requests.get(popcat_url, params={"to": to_language, "text": text})

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "error": "Failed to retrieve translation API."
            }), response.status_code

        # Parse the response and reformat it
        popcat_data = response.json()
        translated_text = popcat_data.get("translated")

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "result": translated_text
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