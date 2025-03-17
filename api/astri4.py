from flask import Flask, jsonify, request
import requests
import json

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

        # Extract and format the data, defaulting to None for missing keys
        formatted_data = {
            "title": external_data.get("title", None),
            "duration": external_data.get("duration", None),
            "quality": external_data.get("quality", None),
            "thumbnail": external_data.get("thumbnail", None),
            "download": external_data.get("download", None)
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

        # Extract and format the data, defaulting to None for missing keys
        formatted_data = {
            "desc": external_data.get("desc", None),
            "thumb": external_data.get("thumb", None),
            "video_sd": external_data.get("video_sd", None),
            "video_hd": external_data.get("video_hd", None),
            "audio": external_data.get("audio", None)
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
        
        data = response.json().get("data", {})

        # Check if the user profile exists
        if not data:
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No data found for this user."
            }), 404

        # Construct the profile data
        profile_data = {
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
        }

        # Construct the media data
        media_data = []
        for item in data.get("media", []):
            media_data.append({
                "author": {
                    "username": item.get("author", {}).get("username"),
                    "nickname": item.get("author", {}).get("nickname"),
                    "profile_pic": item.get("author", {}).get("profile_pic"),
                    "upload_at": item.get("author", {}).get("upload_at")
                },
                "title": item.get("title"),
                "media": item.get("media"),
                "retweets": item.get("retweet"),
                "likes": item.get("likes")
            })

        # Combine profile and media data into final result
        results = {
            "profile": profile_data,
            "media": media_data
        }

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
        
# API for spotifydl
@app.route('/api/spotifydl', methods=['GET'])
def spotifydl():
    url = request.args.get('url')
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/spotifydl?url={url}"
    
    try:
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        # Mengambil data 'data' yang berisi string JSON
        external_data_str = response.json().get("data", "")
        
        # Jika ada data, kita parse string JSON tersebut
        if external_data_str:
            external_data = json.loads(external_data_str)

            # Mengambil data yang dibutuhkan
            formatted_data = {
                "channel_name": external_data.get("nama_channel", None),
                "title": external_data.get("judul", None),
                "duration": external_data.get("durasi", None),
                "thumbnail": external_data.get("gambar_kecil", [])[0].get("url", None) if external_data.get("gambar_kecil") else None,
                "download_url": external_data.get("url_audio_v1", None)
            }

            return jsonify({
                "status": 200,
                "creator": "Astri",
                "data": formatted_data
            })
        
        return jsonify({
            "status": 404,
            "creator": "Astri",
            "error": "Data not found in external service response."
        }), 404

    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error occurred: {e}")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

@app.route('/api/youtube/transcript', methods=['GET'])
def transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    # API eksternal
    api_url = f"https://www.itzpire.com/tools/youtube/transcript?url={url}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url)
        response.raise_for_status()
        external_data = response.json()

        # Validasi apakah respons berisi data yang diharapkan
        if "data" not in external_data or not external_data["data"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        # Kembalikan respons yang sudah sesuai format
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["data"]
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
