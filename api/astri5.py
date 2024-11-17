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

        # Assume the external API returns JSON data
        data = response.json()

        # Map the data to match the desired structure
        mapped_response = {
            "data": {
                "location": {
                    "name": data.get("location", {}).get("name", ""),
                    "region": data.get("location", {}).get("region", ""),
                    "country": data.get("location", {}).get("country", ""),
                    "lat": data.get("location", {}).get("lat", 0.0),
                    "lon": data.get("location", {}).get("lon", 0.0),
                    "tz_id": data.get("location", {}).get("tz_id", ""),
                    "localtime_epoch": data.get("location", {}).get("localtime_epoch", 0),
                    "localtime": data.get("location", {}).get("localtime", "")
                },
                "current": {
                    "last_updated_epoch": data.get("current", {}).get("last_updated_epoch", 0),
                    "last_updated": data.get("current", {}).get("last_updated", ""),
                    "temp_c": data.get("current", {}).get("temp_c", 0.0),
                    "temp_f": data.get("current", {}).get("temp_f", 0.0),
                    "is_day": data.get("current", {}).get("is_day", 0),
                    "condition": {
                        "text": data.get("current", {}).get("condition", {}).get("text", ""),
                        "icon": data.get("current", {}).get("condition", {}).get("icon", ""),
                        "code": data.get("current", {}).get("condition", {}).get("code", 0)
                    },
                    "wind_mph": data.get("current", {}).get("wind_mph", 0.0),
                    "wind_kph": data.get("current", {}).get("wind_kph", 0.0),
                    "wind_degree": data.get("current", {}).get("wind_degree", 0),
                    "wind_dir": data.get("current", {}).get("wind_dir", ""),
                    "pressure_mb": data.get("current", {}).get("pressure_mb", 0),
                    "pressure_in": data.get("current", {}).get("pressure_in", 0.0),
                    "precip_mm": data.get("current", {}).get("precip_mm", 0.0),
                    "precip_in": data.get("current", {}).get("precip_in", 0.0),
                    "humidity": data.get("current", {}).get("humidity", 0),
                    "cloud": data.get("current", {}).get("cloud", 0),
                    "feelslike_c": data.get("current", {}).get("feelslike_c", 0.0),
                    "feelslike_f": data.get("current", {}).get("feelslike_f", 0.0),
                    "windchill_c": data.get("current", {}).get("windchill_c", 0.0),
                    "windchill_f": data.get("current", {}).get("windchill_f", 0.0),
                    "heatindex_c": data.get("current", {}).get("heatindex_c", 0.0),
                    "heatindex_f": data.get("current", {}).get("heatindex_f", 0.0),
                    "dewpoint_c": data.get("current", {}).get("dewpoint_c", 0.0),
                    "dewpoint_f": data.get("current", {}).get("dewpoint_f", 0.0),
                    "vis_km": data.get("current", {}).get("vis_km", 0.0),
                    "vis_miles": data.get("current", {}).get("vis_miles", 0.0),
                    "uv": data.get("current", {}).get("uv", 0.0),
                    "gust_mph": data.get("current", {}).get("gust_mph", 0.0),
                    "gust_kph": data.get("current", {}).get("gust_kph", 0.0)
                }
            }
        }

        return jsonify(mapped_response), 200

    except requests.exceptions.Timeout:
        return jsonify({
            "status": 504,
            "creator": "Astri",
            "error": "The request to the external service timed out. Please try again later."
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": 503,
            "creator": "Astri",
            "error": f"Service is unavailable"
        }), 503

if __name__ == "__main__":
    app.run(debug=True)
