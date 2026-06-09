#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.yml -f docker-compose.spark.yml up -d

echo '{"event_id":"evt_bronze_smoke_test","event_type":"order_submitted","event_time":"2026-01-01T00:00:00Z","schema_version":1,"account_id":"acc_0001","order_id":"ord_bronze_smoke_test","symbol":"AAPL","side":"buy","quantity":10,"order_type":"market","status":"submitted","source":"bronze_smoke_test"}' \
| docker exec -i lakehouse-redpanda rpk topic produce order_submitted

docker exec lakehouse-spark spark-submit \
  --properties-file /home/iceberg/conf/spark-defaults.conf \
  /home/iceberg/jobs/write_orders_to_bronze.py

docker exec lakehouse-trino trino --execute \
"SELECT count(*) AS total_rows FROM iceberg.bronze.order_submitted_events"

docker exec lakehouse-trino trino --execute \
"SELECT source_topic, source_partition, source_offset, message_key, raw_payload
 FROM iceberg.bronze.order_submitted_events
 ORDER BY source_offset DESC
 LIMIT 5"
