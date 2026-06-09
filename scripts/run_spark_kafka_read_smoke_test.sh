#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.yml -f docker-compose.spark.yml up -d

echo '{"event_id":"evt_manual_smoke_test","event_type":"order_submitted","event_time":"2026-01-01T00:00:00Z","schema_version":1,"account_id":"acc_0001","order_id":"ord_smoke_test","symbol":"AAPL","side":"buy","quantity":10,"order_type":"market","status":"submitted","source":"spark_kafka_smoke_test"}' \
| docker exec -i lakehouse-redpanda rpk topic produce order_submitted

docker exec lakehouse-spark spark-submit \
  --properties-file /home/iceberg/conf/spark-defaults.conf \
  /home/iceberg/jobs/read_kafka_orders_console.py
