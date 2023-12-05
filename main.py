from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Assuming city_distances is a module providing city distances
from distances import city_distances

def calculate_travel_time(distance, desired_time):
    # Adjust average speed based on distance
    speed_ranges = [(50, 50), (100, 60), (500, 80)]

    for range_start, speed in speed_ranges:
        if distance < range_start:
            average_speed = speed
            break
    else:
        average_speed = 100

    # Calculate predicted travel time (time = distance / speed)
    predicted_time = distance / average_speed

    time_multipliers = {
        (0, 1): 0.9,   # Decrease predicted time by 10% (midnight)
        (1, 2): 0.9,   # Decrease predicted time by 10%
        (2, 3): 0.9,   # Decrease predicted time by 10%
        (3, 4): 0.9,   # Decrease predicted time by 10%
        (4, 5): 0.9,   # Decrease predicted time by 10%
        (5, 6): 0.9,   # Decrease predicted time by 10%
        (6, 7): 1.0,   # Normal predicted time (morning)
        (7, 8): 1.1,   # Slight increase in predicted time
        (8, 9): 1.2,   # Moderate increase in predicted time
        (9, 10): 1.5,  # Significant increase in predicted time
        (10, 11): 1.4,  # Slightly reduced from 9 AM
        (11, 12): 1.3,  # Slightly reduced from 10 AM
        (12, 13): 1.2,  # Slightly reduced from 11 AM
        (13, 14): 1.1,  # Slightly reduced from 12 PM
        (14, 15): 1.0,  # Normal predicted time (afternoon)
        (15, 16): 0.9,  # Slight decrease in predicted time
        (16, 17): 0.9,  # Slight decrease in predicted time
        (17, 18): 1.2,  # Moderate increase in predicted time (evening rush hour)
        (18, 19): 1.3,  # Slightly increased from 5 PM
        (19, 20): 1.4,  # Slightly increased from 6 PM
        (20, 21): 1.3,  # Slightly reduced from 7 PM
        (21, 22): 1.2,  # Slightly reduced from 8 PM
        (22, 23): 1.1,  # Slightly reduced from 9 PM
        (23, 24): 0.9,  # Decrease predicted time by 10% (late night)
    }

    for start, end in time_multipliers:
        if start <= desired_time.hour < end:
            predicted_time *= time_multipliers[(start, end)]
            break

    return round(predicted_time, 2)

def calculate_traffic_variation(hour):
    # Add your logic to calculate traffic variation based on the hour of the day
    # You can use a similar approach as in the original code
    traffic_variation_ranges = {
        (0, 1): -10,
        (1, 2): -10,
        (2, 3): -5,
        (3, 4): -5,
        (4, 5): 0,
        (5, 6): 0,
        (6, 7): 5,
        (7, 8): 10,
        (8, 9): 15,
        (9, 10): 25,
        (10, 11): 20,
        (11, 12): 15,
        (12, 13): 10,
        (13, 14): 5,
        (14, 15): 0,
        (15, 16): -5,
        (16, 17): -5,
        (17, 18): 15,
        (18, 19): 20,
        (19, 20): 25,
        (20, 21): 15,
        (21, 22): 10,
        (22, 23): 5,
        (23, 24): -10,
    }

    for start, end in traffic_variation_ranges:
        if start <= hour < end:
            return traffic_variation_ranges[(start, end)]

    # Default: no variation
    return 0

# Route for predicting travel time between two cities
@app.route('/time', methods=['GET'])
def get_travel_time():
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    desired_time = datetime.datetime.strptime(request.args.get('desired_time'), '%H:%M') if request.args.get('desired_time') else datetime.datetime.now()

    if city1 is None or city2 is None:
        return jsonify({'error': 'City1 and City2 are required parameters'}), 400

    # Generate keys for the lookup
    key1 = f"{city1} to {city2}"
    key2 = f"{city2} to {city1}"

    # Fetch distance from the data
    distance = city_distances.get(key1) or city_distances.get(key2)

    if distance is None:
        return jsonify({'error': f'Distance between {city1} and {city2} not found'}), 404

    # Calculate predicted travel time
    predicted_time = calculate_travel_time(distance, desired_time)

    # Calculate traffic variation
    traffic_variation = calculate_traffic_variation(desired_time.hour)

    return jsonify({
        'city1': city1,
        'city2': city2,
        'distance': distance,
        'predicted_time': predicted_time,
        'traffic_variation': traffic_variation
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
