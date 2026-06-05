import json
import random
import time
import uuid
from datetime import datetime, timezone

from confluent_kafka import Producer
from faker import Faker

fake = Faker()

producer = Producer({
    "bootstrap.servers": "localhost:19092",
})

SYMBOLS = ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "META"]
SIDES = ["buy", "sell"]
ORDER_TYPES = ["market", "limit"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_order_submitted() -> dict:
    account_id = f"acc_{random.randint(1, 100):04d}"
    order_id = f"ord_{uuid.uuid4().hex[:12]}"

    return {
        "event_id": f"evt_{uuid.uuid4().hex}",
        "event_type": "order_submitted",
        "event_time": now_iso(),
        "schema_version": 1,
        "account_id": account_id,
        "order_id": order_id,
        "symbol": random.choice(SYMBOLS),
        "side": random.choice(SIDES),
        "quantity": random.randint(1, 100),
        "order_type": random.choice(ORDER_TYPES),
        "status": "submitted",
        "source": "trading_api",
    }


def make_api_request_log() -> dict:
    return {
        "event_id": f"evt_{uuid.uuid4().hex}",
        "event_type": "api_request_log",
        "event_time": now_iso(),
        "schema_version": 1,
        "account_id": f"acc_{random.randint(1, 100):04d}",
        "endpoint": random.choice(["/v2/orders", "/v2/account", "/v2/positions", "/v2/assets"]),
        "method": random.choice(["GET", "POST"]),
        "status_code": random.choice([200, 200, 200, 201, 400, 401, 429, 500]),
        "latency_ms": random.randint(20, 1500),
        "region": random.choice(["us-east1", "us-central1", "southamerica-east1"]),
    }


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to topic={msg.topic()} "
            f"partition={msg.partition()} offset={msg.offset()}"
        )


def send_event(topic: str, event: dict) -> None:
    producer.produce(
        topic=topic,
        key=event.get("account_id"),
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report,
    )
    producer.poll(0)


def main() -> None:
    while True:
        order_event = make_order_submitted()
        api_event = make_api_request_log()

        send_event("order_submitted", order_event)
        send_event("api_request_log", api_event)

        producer.flush()
        time.sleep(1)


if __name__ == "__main__":
    main()
