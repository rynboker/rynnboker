from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
from gensim.summarization import summarize

app = Flask(__name__)

# API Weather
@app.route('/api/weather', methods=['GET'])
def weather():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    # API eksternal
    api_url = f"https://api.agatz.xyz/api/cuaca?message={message}"
    try:
        # Ambil data dari API eksternal
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()

        if "data" not in external_data or not external_data["data"]:
            return jsonify({
                "status": 502,
                "creator": "Astri",
                "error": "Invalid response from external API."
            }), 502

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": external_data["data"]
        })
    
    except requests.exceptions.RequestException:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable"
        }), 503

# API untuk mengambil ringkasan website
@app.route('/api/aboutwebsite', methods=['GET'])
def aboutwebsite():
    # Ambil URL dari parameter
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Parameter 'url' is required"}), 400

    try:
        # Ambil konten website
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()

        # Gunakan Gensim untuk membuat ringkasan
        try:
            summary = summarize(text_content, word_count=2000)  # Ringkasan hingga 100 kata
        except ValueError:
            summary = "Unable to generate a summary. The text may be too short."

        # Format untuk Discord
        discord_formatted_summary = f"**Summary of [{url}]({url}):**\n```\n{summary}\n```"

        # Kembalikan hasil
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "url": url,
            "summary": summary,
            "discord_formatted": discord_formatted_summary
        })

    except requests.exceptions.RequestException as e:
        # Tangani error dari permintaan website
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": "Service is unavailable."
        }), 503

    except Exception as e:
        # Tangani error umum lainnya
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
