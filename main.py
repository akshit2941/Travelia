from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import datetime


app = Flask(__name__)
CORS(app)

# City distances data
city_distances = {
    'Agartala to Aizawl': 147,
    'Aizawl to Andaman and Nicobar Islands': 1333,
    'Andaman and Nicobar Islands to Andhra Pradesh': 1470,
    'Andhra Pradesh to Arunachal Pradesh': 2060,
    'Arunachal Pradesh to Assam': 286,
    'Assam to Bangalore': 2175,
    'Bangalore to Bhopal': 1144,
    'Bhopal to Bhubaneshwar': 931,
    'Bhubaneshwar to Bihar': 539,
    'Bihar to Chandigarh': 1046,
    'Chandigarh to Chennai': 1995,
    'Chennai to Chhattisgarh': 926,
    'Chhattisgarh to Dadra and Nagar Haveli': 928,
    'Dadra and Nagar Haveli to Daman and Diu': 33,
    'Daman and Diu to Daman': 2,
    'Daman to Dehradun': 1219,
    'Dehradun to Delhi': 201,
    'Delhi to Gangtok': 1127,
    'Gangtok to Ghandinagar': 1664,
    'Ghandinagar to Goa': 893,
    'Goa to Gujarat': 833,
    'Gujarat to Haryana': 901,
    'Haryana to Himachal Pradesh': 326,
    'Himachal Pradesh to Hyderabad': 1612,
    'Hyderabad to Imphal': 1804,
    'Imphal to Itanagar': 256,
    'Itanagar to Jaipur': 1764,
    'Jaipur to Jharkhand': 1023,
    'Jharkhand to Karnataka': 1361,
    'Karnataka to Kashmir': 2097,
    'Kashmir to Kerala': 2591,
    'Kerala to Kohima': 2497,
    'Kohima to Kolkata': 678,
    'Kolkata to Laccadives': 1903,
    'Laccadives to Lucknow': 1939,
    'Lucknow to Madhya Pradesh': 487,
    'Madhya Pradesh to Maharashtra': 470,
    'Maharashtra to Manipur': 1949,
    'Manipur to Meghalaya': 271,
    'Meghalaya to Mizoram': 301,
    'Mizoram to Mumbai': 2127,
    'Mumbai to Nagaland': 2357,
    'Nagaland to NCT': 1919,
    'NCT to New Delhi': 1259,
    'New Delhi to Odisha': 1166,
    'Odisha to Panaji': 1336,
    'Panaji to Patna': 1625,
    'Patna to Pondicherry': 1621,
    'Pondicherry to Port Blair': 1408,
    'Port Blair to Puducherry': 1406,
    'Puducherry to Punjab': 2186,
    'Punjab to Raipur': 1268,
    'Raipur to Rajasthan': 990,
    'Rajasthan to Ranchi': 1191,
    'Ranchi to Shillong': 707,
    'Shillong to Shimla': 1565,
    'Shimla to Sikkim': 1169,
    'Sikkim to Silvassa': 1770,
    'Silvassa to Srinagar': 1546,
    'Srinagar to Tamil Nadu': 2583,
    'Tamil Nadu to Telangana': 778,
    'Telangana to Thiruvananthapuram': 1094,
    'Thiruvananthapuram to Tripura': 2348,
    'Tripura to Uttar Pradesh': 1257,
    'Uttar Pradesh to Uttarakhand': 297,
    'Uttarakhand to West Bengal': 1179,
    'Thiruvananthapuram to Delhi': 2243,
    'Srinagar to Delhi': 647,
    'Shimla to Delhi': 273,
    'Silvassa to Delhi': 1025,
    'Shillong to Delhi': 1489,
    'Ranchi to Delhi': 1002,
    'Raipur to Delhi': 937,
    'Port Blair to Delhi': 2483,
    'Puducherry to Delhi': 1879,
    'Patna to Delhi': 851,
    'Panaji to Delhi': 1504,
    'New Delhi to Delhi': 2,
    'Chennai to Delhi': 1759,
    'Lucknow to Delhi': 416,
    'Kohima to Delhi': 1701,
    'Jaipur to Delhi': 239,
    'Itanagar to Delhi': 1618,
    'Imphal to Delhi': 1713,
    'Hyderabad to Delhi': 1259,
    'Gangtok to Delhi': 1127,
    'Ghandinagar to Delhi': 756,
    'Delhi to Dehradun': 201,
    'Delhi to Bangalore': 2166,
    'Delhi to Daman': 1018,
    'Delhi to Kolkata': 1305,
    'Delhi to Mumbai': 1153,
    'Delhi to Bhubaneshwar': 1275,
    'Delhi to Bhopal': 601,
    'Delhi to Bangalore': 1744,
    'Delhi to Aizawl': 1638,
    'Delhi to Agartala': 1499,
    'West Bengal to Delhi': 1235,
    'Uttar Pradesh to Delhi': 306,
    'Tripura to Delhi': 1560,
    'Telangana to Delhi': 1186,
    'Tamil Nadu to Delhi': 1955,
    'Sikkim to Delhi': 1113,
    'Rajasthan to Delhi': 347,
    'Punjab to Delhi': 332,
    'Pondicherry to Delhi': 1881,
    'Odisha to Delhi': 1167,
    'Nagaland to Delhi': 1732,
    'Mizoram to Delhi': 1684,
    'Meghalaya to Delhi': 1443,
    'Manipur to Delhi': 1714,
    'Maharashtra to Delhi': 1002,
    'Madhya Pradesh to Delhi': 648,
    'Laccadives to Delhi': 2080,
    'Kerala to Delhi': 1982,
    'Karnataka to Delhi': 1491,
    'Kashmir to Delhi': 612,
    'Himachal Pradesh to Delhi': 354,
    'Haryana to Delhi': 120,
    'Gujarat to Delhi': 934,
    'Daman and Diu to Delhi': 1016,
    'Goa to Delhi': 1519,
    'NCT to Delhi': 1261,
    'Dadra and Nagar Haveli to Delhi': 1034,
    'Chandigarh to Delhi': 235,
    'Bihar to Delhi': 894,
    'Assam to Delhi': 1573,
    'Arunachal Pradesh to Delhi': 1710,
    'Andhra Pradesh to Delhi': 1440,
    'Andaman and Nicobar Islands to Delhi': 2470,
    'Chhattisgarh to Delhi': 944,
    'Jharkhand to Delhi': 980,
    'Uttarakhand to Delhi': 234,
    'Jaipur to Thiruvananthapuram': 2053,
    'Jaipur to Srinagar': 803,
    'Jaipur to Shimla': 484,
    'Jaipur to Silvassa': 792,
    'Jaipur to Shillong': 1611,
    'Jaipur to Ranchi': 1040,
    'Jaipur to Raipur': 867,
    'Jaipur to Port Blair': 2453,
    'Jaipur to Puducherry': 1719,
    'Jaipur to Patna': 942,
    'Jaipur to Panaji': 1286,
    'Jaipur to New Delhi': 237,
    'Jaipur to Chennai': 1608,
    'Jaipur to Lucknow': 509,
    'Jaipur to Kohima': 1830,
    'Jaipur to Itanagar': 1764,
    'Jaipur to Imphal': 1830,
    'Jaipur to Hyderabad': 1095,
    'Jaipur to Gangtok': 1269,
    'Jaipur to Ghandinagar': 517,
    'Jaipur to Delhi': 239,
    'Jaipur to Dehradun': 437,
    'Jaipur to Daman': 783,
    'Jaipur to Kolkata': 1358,
    'Jaipur to Mumbai': 922,
    'Jaipur to Bhubaneshwar': 1262,
    'Jaipur to Bhopal': 439,
    'Jaipur to Bangalore': 1562,
    'Jaipur to Aizawl': 1737,
    'Jaipur to Agartala': 1593,
    'Jaipur to West Bengal': 1292,
    'Jaipur to Uttar Pradesh': 432,
    'Jaipur to Tripura': 1659,
    'Jaipur to Telangana': 1034,
    'Jaipur to Tamil Nadu': 1782,
    'Jaipur to Sikkim': 1259,
    'Jaipur to Rajasthan': 156,
    'Jaipur to Punjab': 472,
    'Jaipur to Pondicherry': 1721,
    'Jaipur to Odisha': 1155,
    'Jaipur to Nagaland': 1868,
    'Jaipur to Mizoram': 1776,
    'Jaipur to Meghalaya': 1562,
    'Jaipur to Manipur': 1830,
    'Jaipur to Maharashtra': 797,
    'Jaipur to Madhya Pradesh': 526,
    'Jaipur to Laccadives': 1886,
    'Jaipur to Kerala': 1788,
    'Jaipur to Karnataka': 1290,
    'Jaipur to Kashmir': 810,
    'Jaipur to Himachal Pradesh': 563,
    'Jaipur to Haryana': 240,
    'Jaipur to Gujarat': 696,
}


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

    return jsonify({'city1': city1, 'city2': city2, 'distance': distance, 'predicted_time': predicted_time})

def calculate_travel_time(distance, desired_time):
    # Adjust average speed based on distance
    if distance < 50:
        average_speed = 50
    elif 50 <= distance < 100:
        average_speed = 60
    elif 100 <= distance < 500:
        average_speed = 80
    elif distance >= 500:
        average_speed = 100

    # Calculate predicted travel time (time = distance / speed)
    predicted_time = distance / average_speed

    # Adjust predicted time based on desired time and traffic conditions
    if 7 <= desired_time.hour < 8:
        predicted_time *= 1.1  # Increase predicted time by 10%
    elif 8 <= desired_time.hour < 9:
        predicted_time *= 1.2  # Increase predicted time by 20%
    elif 9 <= desired_time.hour < 10:
        predicted_time *= 1.7  # Increase predicted time by 70%
    elif 10 <= desired_time.hour < 11:
        predicted_time *= 1.4  # Increase predicted time by 40%
    elif 11 <= desired_time.hour < 12:
        predicted_time *= 1.2  # Increase predicted time by 20%
    elif 12 <= desired_time.hour < 13:
        predicted_time *= 1.1  # Increase predicted time by 10%
    elif 13 <= desired_time.hour < 14:
        predicted_time *= 0.9  # Decrease predicted time by 10%
    elif 14 <= desired_time.hour < 15:
        predicted_time *= 0.8  # Decrease predicted time by 20%
    elif 15 <= desired_time.hour < 16:
        predicted_time *= 0.7  # Decrease predicted time by 30%
    elif 16 <= desired_time.hour < 17:
        predicted_time *= 0.9  # Decrease predicted time by 10%
    elif 17 <= desired_time.hour < 18:
        predicted_time *= 1.1  # Increase predicted time by 10%
    elif 18 <= desired_time.hour < 19:
        predicted_time *= 1.3  # Increase predicted time by 30%
    elif 19 <= desired_time.hour < 20:
        predicted_time *= 1.4  # Increase predicted time by 40%
    elif 20 <= desired_time.hour < 21:
        predicted_time *= 1.2  # Increase predicted time by 20%
    elif 21 <= desired_time.hour < 22:
        predicted_time *= 1.1  # Increase predicted time by 10%
    elif 22 <= desired_time.hour < 23:
        predicted_time *= 1.05  # Increase predicted time by 5%
    elif 23 <= desired_time.hour or (0 <= desired_time.hour < 6):
        predicted_time *= 0.9  # Decrease predicted time by 10%
    elif 1 <= desired_time.hour < 2:
        predicted_time *= 0.8  # Decrease predicted time by 20%
    elif 2 <= desired_time.hour < 3:
        predicted_time *= 0.7  # Decrease predicted time by 30%
    elif 3 <= desired_time.hour < 4:
        predicted_time *= 0.6  # Decrease predicted time by 40%
    elif 4 <= desired_time.hour < 5:
        predicted_time *= 0.6  # Decrease predicted time by 40%
    elif 5 <= desired_time.hour < 6:
        predicted_time *= 0.9  # Decrease predicted time by 10%

    return round(predicted_time, 2)


if __name__ == '__main__':
    app.run(debug=True)