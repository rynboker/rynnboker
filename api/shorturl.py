import random
import string
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect
import urllib.parse

app = Flask(__name__)

# In-memory storage for URL mappings
url_mapping = {}

def generate_short_code(length=6):
    """Generate a random alphanumeric short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('originalUrl')
    custom_name = data.get('customName')

    # Validate required parameter
    if not original_url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'originalUrl' is required."
        }), 400

    # Use custom name if provided and unique, otherwise generate a new one
    if custom_name:
        short_code = custom_name
        if short_code in url_mapping:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Custom name already taken."
            }), 400
    else:
        # Generate a unique short code
        short_code = generate_short_code()
        while short_code in url_mapping:
            short_code = generate_short_code()

    # Set expiration date for 1 month from now
    expiration_date = datetime.now() + timedelta(days=30)

    # Store the original URL with the short code and expiration date
    url_mapping[short_code] = {
        "originalUrl": original_url,
        "expirationDate": expiration_date.isoformat()  # Save as ISO string
    }

    # Save to JSON file (or in-memory dictionary)
    save_url_mappings(url_mapping)

    # Construct the short URL using your domain
    short_url = f"https://www.youga.my.id/{short_code}"

    return jsonify({
        "status": "success",
        "author": "Astri",
        "code": 200,
        "data": {
            "originalUrl": original_url,
            "shortUrl": short_url,
            "customName": custom_name or short_code,
            "expirationDate": expiration_date.isoformat()
        }
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    # Load the latest data from the JSON file (or memory)
    global url_mapping
    url_mapping = load_url_mappings()

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
        save_url_mappings(url_mapping)
        return jsonify({
            "status": 410,
            "error": "This short URL has expired."
        }), 410

    # If the URL is still valid, redirect to the original URL
    return redirect(url_data["originalUrl"])

if __name__ == "__main__":
    app.run(debug=True)
