import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/photo2anime2', methods=['GET'])
def photo2anime2():
    # Ambil parameter 'url' dan 'type' dari query string
    image_url = request.args.get('url')
    version = request.args.get('type', 'version 0.2')  # Default ke version 0.2 jika tidak ada
    
    # Validasi URL dan version
    if not image_url:
        return jsonify({"status": 400, "error": "Parameter 'url' is required."}), 400

    if version not in ['version 0.2', 'version 0.3', 'version 0.4']:
        return jsonify({"status": 400, "error": "Invalid 'type' parameter. Valid options are 'version 0.2', 'version 0.3', 'version 0.4'."}), 400

    # Bangun URL API eksternal berdasarkan parameter
    api_url = f"https://itzpire.com/tools/photo2anime2?url={image_url}&type={version}"
    
    try:
        # Kirim request ke API eksternal dengan timeout 10 detik
        response = requests.get(api_url, timeout=10)

        # Cek status code respons
        if response.status_code != 200:
            return jsonify({"status": response.status_code, "error": "External service error."}), response.status_code

        # Parse respons JSON dari API eksternal
        external_data = response.json()
        
        # Debugging: Tampilkan respons untuk debugging
        print(f"Response from external API: {external_data}")
        
        # Cek apakah 'img' ada dalam respons API eksternal
        if "img" in external_data:
            external_img_url = external_data["img"]
            return jsonify({
                "status": 200,
                "result": {
                    "img": external_img_url
                }
            })

        # Jika tidak ada 'img', kirimkan pesan error
        return jsonify({"status": 500, "error": "Image URL not found in response."}), 500

    except requests.exceptions.Timeout:
        # Tangani timeout error
        return jsonify({"status": 504, "error": "Gateway timeout: External service did not respond in time."}), 504
    except requests.exceptions.RequestException as e:
        # Tangani error lain-lain
        return jsonify({"status": 503, "error": f"Service unavailable: {str(e)}"}), 503
    except Exception as e:
        # Tangani error lain-lain
        return jsonify({"status": 500, "error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
