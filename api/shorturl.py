import random
import string
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

# In-memory URL mapping (for Vercel)
url_mapping = {}

def generate_short_code(length=6):
    """Generate a random alphanumeric short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Log input data

        original_url = data.get('originalUrl')
        custom_name = data.get('customName')

        if not original_url:
            return jsonify({
                "status": 400,
                "error": "Parameter 'originalUrl' is required."
            }), 400

        if custom_name:
            short_code = custom_name
            if short_code in url_mapping:
                return jsonify({
                    "status": 400,
                    "error": "Custom name already taken."
                }), 400
        else:
            short_code = generate_short_code()
            while short_code in url_mapping:
                short_code = generate_short_code()

        expiration_date = datetime.now() + timedelta(days=30)

        url_mapping[short_code] = {
            "originalUrl": original_url,
            "expirationDate": expiration_date.isoformat()
        }

        print(f"Created short URL mapping: {short_code} -> {original_url}")  # Log mapping creation

        short_url = f"https://www.youga.my.id/{short_code}"

        return jsonify({
            "status": "success",
            "data": {
                "originalUrl": original_url,
                "shortUrl": short_url,
                "customName": custom_name or short_code,
                "expirationDate": expiration_date.isoformat()
            }
        })

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    print(f"Current URL Mapping: {url_mapping}")  # Debug print

    try:
        # Retrieve the original URL and check if it exists
        url_data = url_mapping.get(short_code)
        
        if not url_data:
            return jsonify({
                "status": 404,
                "error": "Short URL not found."
            }), 404

        # Check if the URL has expired
        expiration_date = datetime.fromisoformat(url_data["expirationDate"])
        if datetime.now() > expiration_date:
            # Remove the expired URL from storage
            del url_mapping[short_code]
            return jsonify({
                "status": 410,
                "error": "This short URL has expired."
            }), 410

        # If the URL is still valid, redirect to the original URL
        return redirect(url_data["originalUrl"])

    except Exception as e:
        # Log the error for debugging
        print(f"Error in redirecting: {e}")
        return jsonify({
            "status": 500,
            "error": "An internal error occurred."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
