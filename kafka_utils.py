from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import dumps, loads

from kafka.structs import (
    TopicPartition
)


producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )

# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='arbitrage_app',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

tp = TopicPartition("odds_topic", 0)
consumer.assign([tp])


def assign_offset_to_consumer(kafka_consumer, offset):
    tp = TopicPartition("odds_topic", 0)
    kafka_consumer.assign([tp])
    kafka_consumer.seek_to_beginning()
    kafka_consumer.seek(tp, offset)


def assign_offset_based_on_timestamp(kafka_consumer, timestamp):
    kafka_consumer.seek_to_beginning()
    rec_in = kafka_consumer.offsets_for_times({tp: timestamp})
    kafka_consumer.seek(tp, rec_in[tp].offset)