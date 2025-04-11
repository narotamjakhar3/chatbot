from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Route to calculate distance using Google Maps API
@app.route('/get_distance', methods=['POST'])
def get_distance():
    # Retrieve from and to locations from the POST request
    data = request.json
    from_location = data.get('from')
    to_location = data.get('to')

    # Google Maps API key (loaded from environment variable for security)
    api_key = "AIzaSyD6I_IKP5hiZ03m9S55DZWS5pw9KWsYwig"  # Replace with your actual key

    # Construct the Distance Matrix API URL
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={from_location}&destinations={to_location}&key={api_key}"

    # Call the Google Maps API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()

        if response_json['rows'] and response_json['rows'][0]['elements'] and response_json['rows'][0]['elements'][0]['status'] == 'OK':
            distance = response_json['rows'][0]['elements'][0]['distance']['text']
            duration = response_json['rows'][0]['elements'][0]['duration']['text']
            return jsonify({'distance': distance, 'duration': duration})
        else:
            # Handle cases where no route is found or the status is not OK
            return jsonify({'error': 'No route found between the specified locations.'}), 400  # Return a 400 Bad Request

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error calling Google Maps API: {e}'}), 500
    except (KeyError, IndexError) as e:
        return jsonify({'error': f'Error parsing Google Maps API response: {e}'}), 500

if __name__ == '__main__':
    app.run(port=5000)

    "AIzaSyD6I_IKP5hiZ03m9S55DZWS5pw9KWsYwig"