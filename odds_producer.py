from json import dumps
from kafka import KafkaProducer
import db_utils

rows = db_utils.select_from_sqlite("SELECT * FROM matches_odds", one=False)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

for row in rows:
    print(dict(row))
    producer.send('odds_topic', value={'data' : dict(row)})