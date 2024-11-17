from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import openai

app = Flask(__name__)

openai.api_key = 'API_KEY_ANDA'

# Konfigurasi API Weather
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
        external_data = response.json()  # Data dari API agatz

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
            "data": external_data["data"]  # Gunakan langsung data dari API eksternal
        })
    
    except requests.exceptions.RequestException as e:
        # Tangani error dari API eksternal
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

# Konfigurasi API OpenAI
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

        # Analisis menggunakan AI (dalam bahasa Inggris)
        prompt = f"Summarize the following text into a brief summary in English:\n\n{text_content}"
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        ai_response = completion.choices[0].text.strip()

        # Format respons untuk Discord
        discord_formatted_summary = f"**Summary of [{url}]({url}):**\n```\n{ai_response}\n```"

        # Kembalikan hasil
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "discord_formatted": discord_formatted_summary,  # Format untuk Discord
            "url": url,
            "summary": ai_response
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
