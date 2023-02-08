import json
from confluent_kafka import Consumer
from dotenv import load_dotenv
import os

load_dotenv()
server = os.getenv("KAFKA_SERVER")
username = os.getenv("KAFKA_KEY")
password = os.getenv("KAFKA_SECRET")


class Kafka:
    def __init__(self):
        self.kafka_topic_name = 'deloton'
        self.consumer: Consumer = Consumer({
            'bootstrap.servers': server,
            'group.id': 'triple-e-consumer',
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': username,
            'sasl.password': password,
            'session.timeout.ms': 6000,
            'heartbeat.interval.ms': 1000,
            'fetch.wait.max.ms': 6000,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': 'false',
            'max.poll.interval.ms': '86400000',
            'topic.metadata.refresh.interval.ms': "-1",
            "client.id": 'id-002-005',
        })
            

    def _print_msg(self, msg):
        print(
        f"""
            topic:{msg.topic()}, key:{msg.key()}, 
            value:{msg.value()}
        """
    )
    
    def _list_topics(self):
        return self.consumer.list_topics()

    def get_data(self, consumer = None, topic_name = None, amount:int = 100_000):
        if consumer is None:
            consumer = self.consumer
        if topic_name is None:
            topic_name = self.kafka_topic_name
            
        consumer.subscribe([topic_name])
        
        values = []
        for i in range(amount):
            msg = consumer.poll(1.0)
            if msg:
                # self._print_msg(msg)
                values.append(json.loads(msg.value().decode('utf-8')))
            
        return values



k = Kafka()
# print(k._list_topics())
data = k.get_data(amount=100000)
json.dump(data, open('./Data/data.json', 'w'))