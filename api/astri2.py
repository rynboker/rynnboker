import random
import string
from datetime import datetime, timedelta
import json
import requests
from flask import Flask, jsonify, request, redirect
import os
import time

app = Flask(__name__)

# Define the path for persistent storage (e.g., in Vercel's file system)
DATABASE_FILE = "/tmp/listurl.json"

# Discord webhook URL for logging
WEBHOOK_URL = "https://discord.com/api/webhooks/1307833033214263371/LwKikJE1Xd_tUMqjmPlXXPEovhWdnanCazOurkqmddrUgCqbYRAoDZTCWIncY-2P2z6O"

# Function to send logs to Discord webhook
def send_log_to_discord(status_code, execution_time, path):
    log_message = {
        "content": f"Request to {path} | Status Code: {status_code} | Execution Time: {execution_time:.2f}s"
    }
    try:
        requests.post(WEBHOOK_URL, json=log_message)
    except requests.exceptions.RequestException as e:
        print("Error sending log to Discord:", e)

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

# Log before and after processing each request
def log_request(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        path = request.path

        # Execute the request function
        response = func(*args, **kwargs)

        execution_time = time.time() - start_time

        # Log the details
        send_log_to_discord(response.status_code, execution_time, path)

        return response

    return wrapper
    
@app.route('/api/shorturl', methods=['POST'])
@log_request
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
        print(f"Error occurred")
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

@app.route('/<short_code>', methods=['GET'])
@log_request
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

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": "Error occurred"
        }), 500

@app.route('/api/spotify', methods=['GET'])
@log_request
def spotify():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/spotify?message={message}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "trackNumber": item.get("trackNumber"),
                "trackName": item.get("trackName"),
                "artistName": item.get("artistName"),
                "albumName": item.get("albumName"),
                "duration": item.get("duration"),
                "previewUrl": item.get("previewUrl"),
                "externalUrl": item.get("externalUrl")
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
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

@app.route('/api/threads', methods=['GET'])
@log_request
def threads():
    url = request.args.get('url')

    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/threads?url={url}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        external_data = response.json().get("data", {})
        image_urls = external_data.get("image_urls", [])
        video_urls = external_data.get("video_urls", [])

        formatted_data = {
            "image_urls": image_urls,
            "video_urls": video_urls
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": "An unexpected error occurred"
        }), 500

@app.route('/api/translate', methods=['GET'])
@log_request
def translate_text():
    text = request.args.get('text')
    to_language = request.args.get('to', 'en')

    if not text:
        return jsonify({
            "status": 400,
            "error": "Parameter 'text' is required."
        }), 400

    popcat_url = "https://api.popcat.xyz/translate"
    try:
        response = requests.get(popcat_url, params={"to": to_language, "text": text})

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "error": "Failed to retrieve translation API."
            }), response.status_code

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
            "error": f"Service is unavailable"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500

@app.route('/api/ttstalk', methods=['GET'])
@log_request
def ttstalk():
    name = request.args.get('name')

    if not name:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'name' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ttstalk?name={name}"
    try:
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        try:
            external_data = response.json()
            
            # Check if the response is a dictionary and contains the "data" field
            if isinstance(external_data, dict) and "data" in external_data:
                external_data = external_data["data"]
            else:
                return jsonify({
                    "status": 404,
                    "creator": "Astri",
                    "error": "No valid data found for the specified name."
                }), 404

        except ValueError as e:
            app.logger.error(f"Error parsing JSON")
            return jsonify({
                "status": 500,
                "creator": "Astri",
                "error": "Failed to parse the response from the external service."
            }), 500

        # Format data as expected
        formatted_data = {
            "photo": external_data.get("photo"),
            "username": external_data.get("username"),
            "name": external_data.get("name"),
            "bio": external_data.get("bio"),
            "followers": external_data.get("followers"),
            "following": external_data.get("following"),
            "likes": external_data.get("likes"),
            "posts": external_data.get("posts")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        app.logger.error(f"RequestException")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

    except Exception as e:
        app.logger.error(f"Unexpected error")
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred"
        }), 500
        
if __name__ == "__main__":
    app.run(debug=True)
