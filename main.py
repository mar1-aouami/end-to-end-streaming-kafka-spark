import os 
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
import random
import uuid
import time

ROUTE_WAYPOINTS = [
    {"latitude": 35.7767, "longitude": -5.80389},
    {"latitude": 35.1932, "longitude": -6.1557},
    {"latitude": 34.2541, "longitude": -6.5890},
    {"latitude": 33.9716, "longitude": -6.8498},
    {"latitude": 33.5883, "longitude": -7.6114}
]

current_waypoint_index = 0
start_location = ROUTE_WAYPOINTS[0].copy()
STEPS_PER_SEGMENT = 25

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

start_time = datetime.now()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40),
        'direction': 'South-West',
        'vehicleType': vehicle_type
    }

def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'location': location,
        'cameraId': camera_id,
        'snapshot': "https://bostonglobe-prod.cdn.arcpublishing.com/camera.jpg"
    }

def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'device_Id': device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(15, 30),
        'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rain']),
        'precipitation': random.uniform(0, 5),
        'windSpeed': random.uniform(5, 20),
        'humidity': random.randint(40, 80),
        'AirQualityIndex': random.uniform(20, 100)
    }

def generate_emergency_incident_data(device_id, timestamp, location):
    incident_type = random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None'])
    return {
        'id': uuid.uuid4(),
        'device_Id': device_id,
        'incidentId': uuid.uuid4(),
        'timestamp': timestamp,
        'location': location,
        'type': incident_type,
        'status': 'Active' if incident_type != 'None' else 'None',
        'description': f'Emergency {incident_type} reported'
    }

def simulate_vehicle_movement():
    global start_location, current_waypoint_index

    if current_waypoint_index < len(ROUTE_WAYPOINTS) - 1:
        current_pt = ROUTE_WAYPOINTS[current_waypoint_index]
        next_pt = ROUTE_WAYPOINTS[current_waypoint_index + 1]
        
        lat_inc = (next_pt['latitude'] - current_pt['latitude']) / STEPS_PER_SEGMENT
        lon_inc = (next_pt['longitude'] - current_pt['longitude']) / STEPS_PER_SEGMENT
        
        start_location['latitude'] += lat_inc + random.uniform(-0.0005, 0.0005)
        start_location['longitude'] += lon_inc + random.uniform(-0.0005, 0.0005)
        
        if (lat_inc < 0 and start_location['latitude'] <= next_pt['latitude']) or \
           (lat_inc > 0 and start_location['latitude'] >= next_pt['latitude']):
            current_waypoint_index += 1
            start_location = ROUTE_WAYPOINTS[current_waypoint_index].copy()
            
    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(60, 120),
        'direction': 'South-West',
        'make': 'BMW',
        'model': 'X7',
        'year': 2025,
        'fueltype': 'Hybrid'
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Type {obj.__class__.__name__} not serializable')

def delivery_report(err, msg):
    if err is None:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        t, loc = vehicle_data['timestamp'], vehicle_data['location']
        
        for topic, data in [
            (VEHICLE_TOPIC, vehicle_data),
            (GPS_TOPIC, generate_gps_data(device_id, t)),
            (TRAFFIC_TOPIC, generate_traffic_camera_data(device_id, t, loc, 'cam123')),
            (WEATHER_TOPIC, generate_weather_data(device_id, t, loc)),
            (EMERGENCY_TOPIC, generate_emergency_incident_data(device_id, t, loc))
        ]:
            producer.produce(
                topic,
                key=str(data['id']),
                value=json.dumps(data, default=json_serializer).encode('utf-8'),
                on_delivery=delivery_report
            )

        if current_waypoint_index >= len(ROUTE_WAYPOINTS) - 1:
            print("Target reached: Casablanca. Stopping simulation...")
            producer.flush()
            break

        producer.flush()
        time.sleep(5)

if __name__ == "__main__":
    producer = SerializingProducer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    try:
        simulate_journey(producer, 'vehicle_123')
    except KeyboardInterrupt:
        print('Stopped by user')