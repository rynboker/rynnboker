from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# API for soundcloud
@app.route('/api/soundcloud', methods=['GET'])
def soundcloud():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/soundcloud?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        data = response.json()
        results = []
        for item in data.get("data", []):
            results.append({
                "link": item.get("link"),
                "title": item.get("judul")
            })
        
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

# API for soundclouddl
@app.route('/api/soundclouddl', methods=['GET'])
def soundclouddl():
    url = request.args.get('url')
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/soundclouddl?url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        # Get the response data (the 'data' field is an object, not a list)
        external_data = response.json().get("data", {})

        # Ensure that 'data' is a valid object with the expected keys
        if not isinstance(external_data, dict) or not all(key in external_data for key in ["title", "duration", "quality", "thumbnail", "download"]):
            return jsonify({
                "status": 500,
                "creator": "Astri",
                "error": "Unexpected response format from external API."
            }), 500

        # Extract and format the data
        formatted_data = {
            "title": external_data.get("title"),
            "duration": external_data.get("duration"),
            "quality": external_data.get("quality"),
            "thumbnail": external_data.get("thumbnail"),
            "download": external_data.get("download")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

# API for twitter
@app.route('/api/twitter', methods=['GET'])
def twitter():
    url = request.args.get('url')
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/twitter?url={url}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        # Get the response data (the 'data' field is an object, not a list)
        external_data = response.json().get("data", {})

        # Ensure that 'data' is a valid object with the expected keys
        if not isinstance(external_data, dict) or not all(key in external_data for key in ["title", "duration", "quality", "thumbnail", "download"]):
            return jsonify({
                "status": 500,
                "creator": "Astri",
                "error": "Unexpected response format from external API."
            }), 500

        # Extract and format the data
        formatted_data = {
            "audio": external_data.get("audio"),
            "video_hd": external_data.get("video_hd"),
            "video_sd": external_data.get("video_sd"),
            "thumb": external_data.get("thumb"),
            "desc": external_data.get("desc")
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

# API for twitterstalk
@app.route('/api/twitterstalk', methods=['GET'])
def twitterstalk():
    name = request.args.get('name')
    if not name:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'name' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/twitterstalk?name={name}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        data = response.json()
        if not data.get("media"):
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No media found for this user."
            }), 404

        results = {
            "profile": {
                "username": data.get("username"),
                "nickname": data.get("nickname"),
                "background": data.get("background"),
                "profile_pic": data.get("profile"),
                "description": data.get("desc_text"),
                "join_at": data.get("join_at"),
                "map": data.get("map"),
                "tweets_count": data.get("tweets_count"),
                "followers": data.get("followers"),
                "following": data.get("following"),
                "media_count": data.get("media_count")
            },
            "media": []
        }

        for item in data.get("media", []):
            results["media"].append({
                "author": {
                    "username": item["author"].get("username"),
                    "nickname": item["author"].get("nickname"),
                    "profile_pic": item["author"].get("profile_pic"),
                    "upload_at": item["author"].get("upload_at")
                },
                "title": item.get("title"),
                "media": item.get("media"),
                "retweets": item.get("retweet"),
                "likes": item.get("likes")
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
