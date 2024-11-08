import random
import string
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

# In-memory URL mapping (or load from JSON)
url_mapping = {}

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Endpoint to create a short URL
@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('originalUrl')
    custom_name = data.get('customName')

    if not original_url:
        return jsonify({"status": 400, "error": "Parameter 'originalUrl' is required."}), 400

    short_code = custom_name if custom_name else generate_short_code()
    if short_code in url_mapping:
        return jsonify({"status": 400, "error": "Custom name already taken."}), 400

    # Store URL with expiration
    expiration_date = datetime.now() + timedelta(days=30)
    url_mapping[short_code] = {
        "originalUrl": original_url,
        "expirationDate": expiration_date.isoformat()
    }

    short_url = f"http://www.youga.my.id/{short_code}"
    return jsonify({
        "status": "success",
        "shortUrl": short_url,
        "expirationDate": expiration_date.isoformat()
    })

# Endpoint to handle redirects for short URLs
@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    url_data = url_mapping.get(short_code)
    if not url_data:
        return jsonify({"status": 404, "error": "Short URL not found."}), 404

    expiration_date = datetime.fromisoformat(url_data["expirationDate"])
    if datetime.now() > expiration_date:
        return jsonify({"status": 410, "error": "Short URL expired."}), 410

    return redirect(url_data["originalUrl"])

if __name__ == "__main__":
    app.run(debug=True)
    
