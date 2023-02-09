import json
import time
from confluent_kafka import Consumer
from dotenv import load_dotenv
import os
import re
import ast
import uuid
from consumer import get_msg, format_data
import datetime

load_dotenv(override=True)
server = os.getenv("KAFKA_SERVER")
username = os.getenv("KAFKA_KEY")
password = os.getenv("KAFKA_SECRET")


def kafka_consumer() -> Consumer:
    """Makes a connection to a Kafka consumer"""
    c = Consumer({
        "bootstrap.servers": os.getenv("KAFKA_SERVER"),
        "group.id": f"deloton_stream" + str(uuid.uuid1()),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.getenv("KAFKA_KEY"),
        "sasl.password": os.getenv("KAFKA_SECRET"),
        "fetch.wait.max.ms": 6000,
        "auto.offset.reset": "latest",
        "enable.auto.commit": "false",
        "max.poll.interval.ms": "86400000",
        "topic.metadata.refresh.interval.ms": "-1",
        "client.id": "id-002-00eee",
    })
    c.subscribe(["deloton"])
    return c

consumer = kafka_consumer()


get_msg(consumer)

# while True:
#     time.sleep(2)
#     name, age, gender,duration,resistance,hrt,rpm,power = format_data(consumer)

#     print(f'the user is: {name}, {age}, {gender}')
#     print(f'duration: {duration}, resistance: {resistance}')
#     print(f'hrt: {hrt}, rpm: {rpm}, power: {power}')
