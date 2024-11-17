from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/cuaca', methods=['GET'])
def cuaca():
    message = request.args.get('message')
    if not message:
        return jsonify({
            "status": 400,
            "creator": "Astri",
            "error": "Parameter 'message' is required."
        }), 400

    api_url = f"https://api.agatz.xyz/api/cuaca?message={message}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        external_data = response.json()

        # Map external data to desired structure
        mapped_response = {
            "status": 200,
            "creator": "Astri",
            "data": {
                "location": {
                    "name": external_data.get("location", {}).get("name", ""),
                    "region": external_data.get("location", {}).get("region", ""),
                    "country": external_data.get("location", {}).get("country", ""),
                    "lat": external_data.get("location", {}).get("lat", 0.0),
                    "lon": external_data.get("location", {}).get("lon", 0.0),
                    "tz_id": external_data.get("location", {}).get("tz_id", ""),
                    "localtime_epoch": external_data.get("location", {}).get("localtime_epoch", 0),
                    "localtime": external_data.get("location", {}).get("localtime", "")
                },
                "current": {
                    "last_updated_epoch": external_data.get("current", {}).get("last_updated_epoch", 0),
                    "last_updated": external_data.get("current", {}).get("last_updated", ""),
                    "temp_c": external_data.get("current", {}).get("temp_c", 0.0),
                    "temp_f": external_data.get("current", {}).get("temp_f", 0.0),
                    "is_day": external_data.get("current", {}).get("is_day", 1),
                    "condition": {
                        "text": external_data.get("current", {}).get("condition", {}).get("text", ""),
                        "icon": external_data.get("current", {}).get("condition", {}).get("icon", ""),
                        "code": external_data.get("current", {}).get("condition", {}).get("code", 0)
                    },
                    "wind_mph": external_data.get("current", {}).get("wind_mph", 0.0),
                    "wind_kph": external_data.get("current", {}).get("wind_kph", 0.0),
                    "wind_degree": external_data.get("current", {}).get("wind_degree", 0),
                    "wind_dir": external_data.get("current", {}).get("wind_dir", ""),
                    "pressure_mb": external_data.get("current", {}).get("pressure_mb", 0),
                    "pressure_in": external_data.get("current", {}).get("pressure_in", 0.0),
                    "precip_mm": external_data.get("current", {}).get("precip_mm", 0.0),
                    "precip_in": external_data.get("current", {}).get("precip_in", 0.0),
                    "humidity": external_data.get("current", {}).get("humidity", 0),
                    "cloud": external_data.get("current", {}).get("cloud", 0),
                    "feelslike_c": external_data.get("current", {}).get("feelslike_c", 0.0),
                    "feelslike_f": external_data.get("current", {}).get("feelslike_f", 0.0),
                    "uv": external_data.get("current", {}).get("uv", 0.0),
                    "gust_mph": external_data.get("current", {}).get("gust_mph", 0.0),
                    "gust_kph": external_data.get("current", {}).get("gust_kph", 0.0)
                }
            }
        }

        return jsonify(mapped_response), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable: {str(e)}"
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
