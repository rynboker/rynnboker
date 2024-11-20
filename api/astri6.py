from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Function to upload file to Catbox
def upload_to_catbox(file_content, file_name):
    url = "https://catbox.moe/user/api.php"
    files = {
        'reqtype': (None, 'fileupload'),
        'fileToUpload': (file_name, file_content)
    }
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.text  # Catbox returns the file URL as plain text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to upload to Catbox: {e}")

@app.route('/api/musicsearch', methods=['GET'])
def music_search():
    # Ambil parameter 'file' dari request
    file_url = request.args.get('file')
    
    if not file_url:
        return jsonify({"error": "Parameter 'file' is required"}), 400
    
    try:
        # Download the file from Discord
        file_response = requests.get(file_url, stream=True)
        file_response.raise_for_status()  # Raise an error for invalid responses

        # Get the file name from Discord URL (or assign a default name)
        file_name = file_url.split('/')[-1].split('?')[0] or "file_from_discord"
        
        # Upload file to Catbox
        catbox_url = upload_to_catbox(file_response.content, file_name)
        
        # Use the Catbox URL to fetch music information
        lolhuman_url = "https://api.lolhuman.xyz/api/musicsearch"
        params = {
            "apikey": "59485720964df592a349c173",
            "file": catbox_url
        }
        
        # Send request to the music API
        music_response = requests.get(lolhuman_url, params=params)
        music_response.raise_for_status()
        music_data = music_response.json()
        
        # Transform the response into the desired format
        result = {
            "creator": "Astri",
            "status": music_response.status_code,
            "result": {
                "title": music_data.get("title", ""),
                "album": music_data.get("album", ""),
                "artists": music_data.get("artists", []),
                "duration": music_data.get("duration", 0),
                "release": music_data.get("release", ""),
                "genres": music_data.get("genres", [])
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        # Handle errors
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
