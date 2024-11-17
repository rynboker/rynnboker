from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1307833033214263371/LwKikJE1Xd_tUMqjmPlXXPEovhWdnanCazOurkqmddrUgCqbYRAoDZTCWIncY-2P2z6O"

def send_discord_log(message, level="INFO"):
    """Send a log message to a Discord webhook."""
    embed_color = {
        "INFO": 3447003,  # Blue
        "WARNING": 16776960,  # Yellow
        "ERROR": 15158332  # Red
    }
    payload = {
        "embeds": [
            {
                "title": f"Log Level: {level}",
                "description": message,
                "color": embed_color.get(level, 3447003)
            }
        ]
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send log to Discord: {e}")

# API for weather
@app.route('/api/weather', methods=['GET'])
def weather():
    message = request.args.get('message')
    if not message or message.strip() == "":
        error_message = "Parameter 'message' is required and cannot be empty."
        send_discord_log(error_message, "WARNING")
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": error_message
        }), 400

    api_url = f"https://api.agatz.xyz/api/cuaca?message={message}"
    try:
        # Log the request to Discord
        send_discord_log(f"Sending request to external API: {api_url}", "INFO")

        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        # Log successful response to Discord
        send_discord_log(f"Response received: {response.status_code} - {response.text}", "INFO")

        data = response.json()
        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": data
        })

    except requests.exceptions.Timeout:
        error_message = "The request to the external service timed out. Please try again later."
        send_discord_log(error_message, "ERROR")
        return jsonify({
            "status": 504,
            "creator": "Astri",
            "error": error_message
        }), 504

    except requests.exceptions.RequestException as e:
        error_message = f"Service is unavailable: {str(e)}"
        send_discord_log(error_message, "ERROR")
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": error_message
        }), 503

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
