import random
import string
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

# In-memory URL mappings
url_mapping = {}

def generate_short_code(length=6):
    """Generate a random alphanumeric short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('originalUrl')
    custom_name = data.get('customName')

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
        short_code = generate_short_code()
        while short_code in url_mapping:
            short_code = generate_short_code()

    # Set expiration date for 1 month from now
    expiration_date = datetime.now() + timedelta(days=30)

    # Encode URL to handle special characters
    encoded_url = urllib.parse.quote(original_url, safe='')

    url_mapping[short_code] = {
        "originalUrl": encoded_url,
        "expirationDate": expiration_date.isoformat()
    }

    short_url = f"http://www.youga.my.id/{short_code}"

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
    url_data = url_mapping.get(short_code)
    
    if not url_data:
        return jsonify({
            "status": 404,
            "error": "Short URL not found."
        }), 404

    expiration_date = datetime.fromisoformat(url_data["expirationDate"])
    if datetime.now() > expiration_date:
        del url_mapping[short_code]
        return jsonify({
            "status": 410,
            "error": "This short URL has expired."
        }), 410

    # Decode the URL back to its original form
    original_url = urllib.parse.unquote(url_data["originalUrl"])
    return redirect(original_url)

if __name__ == "__main__":
    app.run(debug=True)
