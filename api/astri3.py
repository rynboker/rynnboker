from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# API /api/ytsearch
@app.route('/api/ytsearch', methods=['GET'])
def ytsearch():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytsearch?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        results = [
            {
                "type": item.get("type"),
                "videoId": item.get("videoId"),
                "url": item.get("url"),
                "title": item.get("title"),
                "description": item.get("description"),
                "image": item.get("image"),
                "thumbnail": item.get("thumbnail"),
                "seconds": item.get("seconds"),
                "timestamp": item.get("timestamp"),
                "duration": {
                    "second": item.get("duration", {}).get("second"),
                    "timestamp": item.get("duration", {}).get("timestamp")
                },
                "views": item.get("views"),
                "ago": item.get("ago"),
                "author": {
                    "name": item.get("author", {}).get("name"),
                    "url": item.get("author", {}).get("url")
                }
            }
            for item in data.get("data", [])
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


# API /api/ytplayvid
@app.route('/api/ytplayvid', methods=['GET'])
def ytplayvid():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytplayvid?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json().get("data", {})

        result = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "title": data.get("title"),
                "description": data.get("description"),
                "url": data.get("url"),
                "duration": data.get("duration"),
                "views": data.get("views"),
                "uploadedAt": data.get("uploadedAt"),
                "author": data.get("author"),
                "downloadUrl": data.get("downloadUrl")
            }
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


# API /api/ytplayaud
@app.route('/api/ytplayaud', methods=['GET'])
def ytplayaud():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/ytplay?message={message}"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        info = data.get("data", {}).get("info", {})
        audio = data.get("data", {}).get("audio", {})

        result = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "success": data.get("data", {}).get("success", False),
                "info": {
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "views": info.get("views"),
                    "author": {
                        "name": info.get("author", {}).get("name"),
                        "url": info.get("author", {}).get("url")
                    },
                    "thumbnail": info.get("thumbnail"),
                    "uploaded": info.get("uploaded"),
                    "duration": info.get("duration"),
                    "url": info.get("url")
                },
                "audio": {
                    "size": audio.get("size"),
                    "format": audio.get("format"),
                    "url": audio.get("url")
                }
            }
        }

        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


# API /api/otakudesu
@app.route('/api/otakudesu', methods=['GET'])
def otakudesu():
    message = request.args.get('message')

    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/otakudesu?message={message}"
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
            genre_list = item.get("genre_list", [])
            # Ensure genre_list is a list of dictionaries
            if isinstance(genre_list, list):
                genres = [{"genre_title": genre.get("genre_title"),
                           "genre_link": genre.get("genre_link"),
                           "genre_id": genre.get("genre_id")} for genre in genre_list if isinstance(genre, dict)] or None
            else:
                genres = None

            results.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "link": item.get("link"),
                "id": item.get("id"),
                "status": item.get("status"),
                "score": item.get("score"),
                "genre": genres
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": results
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


# API /api/otakulatest
@app.route('/api/otakudesulatest', methods=['GET'])
def otakulatest():
    api_url = f"https://api.agatz.xyz/api/otakulatest"
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        data = response.json()
        results_on_going = []
        results_complete = []

        for item in data.get("data", {}).get("home", {}).get("on_going", []):
            results_on_going.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "day_updated": item.get("day_updated"),
                "link": item.get("link")
            })

        for item in data.get("data", {}).get("home", {}).get("complete", []):
            results_complete.append({
                "thumb": item.get("thumb"),
                "title": item.get("title"),
                "id": item.get("id"),
                "episode": item.get("episode"),
                "uploaded_on": item.get("uploaded_on"),
                "score": item.get("score"),
                "link": item.get("link")
            })

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "on_going": results_on_going,
            "complete": results_complete
        })

    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable. Please try again later."
        }), 503


if __name__ == '__main__':
    app.run(debug=True)
