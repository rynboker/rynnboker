import requests
from flask import Flask, jsonify, request

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
        response = requests.get(api_url)

        # Handle non-200 responses from the external API
        if response.status_code != 200:
            return jsonify({
                "status": response.status_code,
                "creator": "Astri",
                "error": "Sorry, an error occurred with our external service. Please try again later."
            }), response.status_code

        # Extract and format the data
        external_data = response.json().get("data", [])
        formatted_data = [
            {
                "description": item.get("description"),
                "b": item.get("b"),
                "favicon": item.get("favicon"),
                "is_cloudflare": item.get("is_cloudflare"),
                "summary": item.get("summary"),
                "title": item.get("title"),
                "tokens_input": item.get("tokens_input"),
                "tokens_output": item.get("tokens_output"),
                "tokens_total": item.get("tokens_total")
            }
            for item in external_data
        ]

        return jsonify({
            "status": 200,
            "creator": "Astri",
            "data": formatted_data
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable: {str(e)}"
        }), 503

    except Exception as e:
        return jsonify({
            "status": 500,
            "creator": "Astri",
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)