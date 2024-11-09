import requests
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/api/aboutwebsite', methods=['GET'])
def aboutwebsite():
    url = request.args.get('url')

    # Validate the required parameter
    if not url:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'url' is required."
        }), 400

    # Call the external website information API
    api_url = f"https://itzpire.com/tools/about-website?url={url}"
    try:
        start_time = time.time()  # Mulai pengukuran waktu
        response = requests.get(api_url, timeout=60)  # Timeout lebih panjang

        elapsed_time = time.time() - start_time  # Hitung waktu yang dibutuhkan

        # Handle non-200 responses from the external API
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        # Informasikan jika proses memakan waktu lebih lama
        if elapsed_time > 30:
            return jsonify({
                "status": 200,
                "creator": "Astri",
                "warning": "The external API took longer than usual to respond.",
                "data": response.json().get("data", {})
            })

        # Extract and format the data
        external_data = response.json().get("data", {})

        formatted_data = {
            "description": external_data.get("description", ""),
            "b": external_data.get("b", False),
            "favicon": external_data.get("favicon", ""),
            "is_cloudflare": external_data.get("is_cloudflare", False),
            "summary": external_data.get("summary", ""),
            "title": external_data.get("title", ""),
            "tokens_input": external_data.get("tokens_input", 0),
            "tokens_output": external_data.get("tokens_output", 0),
            "tokens_total": external_data.get("tokens_total", 0)
        }

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "status": 504,
            "creator": "Astri",
            "error": "The external API timed out. Please try again later."
        }), 504

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

if __name__ == "__main__":
    app.run(debug=True)
