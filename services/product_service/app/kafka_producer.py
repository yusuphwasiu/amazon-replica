import asyncio
from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")  # Update with your Kafka broker URL

class KafkaProducer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_product_update(self, product_id: int, action: str):
        message = {
            "product_id": product_id,
            "action": action
        }
        await self.producer.send_and_wait("product_updates", json.dumps(message).encode("utf-8")) 