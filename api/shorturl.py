import random
import string
from datetime import datetime, timedelta
import json
from flask import Flask, jsonify, request, redirect
import os

app = Flask(__name__)

# Define the path for persistent storage (e.g., in Vercel's file system)
DATABASE_FILE = "/tmp/listurl.json"

# Function to load URL mappings from the file
def load_url_mappings():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

# Function to save URL mappings to the file
def save_url_mappings(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to generate short URL codes
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/api/shorturl', methods=['POST'])
def create_short_url():
    try:
        data = request.get_json()
        original_url = data.get('originalUrl')
        custom_name = data.get('customName')

        if not original_url:
            return jsonify({
                "status": 400,
                "error": "Parameter 'originalUrl' is required."
            }), 400

        url_mapping = load_url_mappings()

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

        save_url_mappings(url_mapping)

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
        print(f"Error occurred: {str(e)}")  # Log the error for debugging
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    try:
        url_mapping = load_url_mappings()
        url_data = url_mapping.get(short_code)

        if not url_data:
            return jsonify({
                "status": 404,
                "error": "Short URL not found."
            }), 404

        expiration_date = datetime.fromisoformat(url_data["expirationDate"])
        if datetime.now() > expiration_date:
            del url_mapping[short_code]
            save_url_mappings(url_mapping)
            return jsonify({
                "status": 410,
                "error": "This short URL has expired."
            }), 410

        return redirect(url_data["originalUrl"])

    except Exception as e: # Log the error for debugging
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
