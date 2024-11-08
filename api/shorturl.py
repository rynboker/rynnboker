import random
import string
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)

# Path to the JSON file for storing URL mappings
DATABASE_FILE = "listurl.json"

# Load URL mappings from JSON file
def load_url_mappings():
    try:
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dictionary if file doesn't exist or is corrupted

# Save URL mappings to JSON file
def save_url_mappings(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize URL mappings from the JSON file
url_mapping = load_url_mappings()

# Generate a random short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    try:
        # Parse JSON request body
        data = request.get_json()
        print("Received data:", data)  # Debugging line

        # Extract original URL and custom name
        original_url = data.get('originalUrl')
        custom_name = data.get('customName')

        # Validate required 'originalUrl' parameter
        if not original_url:
            return jsonify({
                "status": 400,
                "creator": "Astri",
                "error": "Parameter 'originalUrl' is required."
            }), 400

        # Use custom name if provided and unique, else generate a unique short code
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

        # Store the original URL, short code, and expiration date
        url_mapping[short_code] = {
            "originalUrl": original_url,
            "expirationDate": expiration_date.isoformat()  # ISO string format
        }

        # Save to JSON file
        save_url_mappings(url_mapping)

        # Construct short URL (replace 'yourdomain.com' with actual domain)
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

    except Exception as e:
        print("Error:", e)  # Debugging line to log the exception
        return jsonify({
            "status": 500,
            "error": "Internal server error."
        }), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    global url_mapping
    url_mapping = load_url_mappings()

    # Retrieve URL data and check existence
    url_data = url_mapping.get(short_code)
    
    if not url_data:
        return jsonify({
            "status": 404,
            "error": "Short URL not found."
        }), 404

    # Check if the URL has expired
    expiration_date = datetime.fromisoformat(url_data["expirationDate"])
    if datetime.now() > expiration_date:
        # Remove expired URL from storage
        del url_mapping[short_code]
        save_url_mappings(url_mapping)
        return jsonify({
            "status": 410,
            "error": "This short URL has expired."
        }), 410

    # If URL is still valid, return original URL
    return jsonify({
        "status": "success",
        "originalUrl": url_data["originalUrl"]
    })

if __name__ == "__main__":
    app.run(debug=True)
