import json, time, random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_record():
    return {
        'sensor_id': random.randint(1, 5),
        'timestamp': int(time.time()),
        'value': random.normalvariate(50, 10)
    }

if __name__ == '__main__':
    while True:
        record = generate_record()
        producer.send('sensor-data', record)
        print(f"Produced: {record}")
        time.sleep(1)
