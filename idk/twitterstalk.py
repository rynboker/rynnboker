from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/idk/twitterstalk', methods=['GET'])
def twitterstalk():
    # Ambil parameter 'name' dari request
    name = request.args.get('name')

    # Validasi parameter
    if not name:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'name' is required."
        }), 400

    # Panggil API eksternal untuk mencari data twitter berdasarkan 'name'
    api_url = f"https://api.agatz.xyz/api/twitterstalk?name={name}"
    try:
        response = requests.get(api_url)
        # Jika respons dari API eksternal tidak berhasil
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code
        
        # Ambil data dari respons API eksternal
        data = response.json()

        # Pastikan ada data yang diinginkan dalam response
        if not data.get("media"):
            return jsonify({
                "status": 404,
                "creator": "Astri",
                "error": "No media found for this user."
            }), 404

        # Buat respons sesuai dengan format yang diinginkan
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

        # Loop through the 'media' array and add each media item
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
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "data": results
        })
    except requests.exceptions.RequestException as e:
        # Tangani error jaringan atau server
        print(f"Error occurred")
        return jsonify({
            "status": 503,
            "creator": "Astri",  # Ganti dengan nama creator kamu
            "error": "Service is unavailable. Please try again later."
        }), 503