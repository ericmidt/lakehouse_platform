# Lakehouse Platform Progress

## Current phase

Stopped at Phase 4: adding Iceberg and Trino.

## Completed so far

- Created initial project structure.
- Added local Redpanda as a Kafka-compatible broker.
- Added Redpanda Console for topic and message inspection.
- Added MinIO as local object storage.
- Added synthetic Python producer for brokerage-style events.
- Created initial Kafka topics:
  - order_submitted
  - order_filled
  - trade_executed
  - api_request_log

## Current local architecture

Python event generator -> Redpanda topics -> future Spark Structured Streaming -> future Iceberg tables on MinIO -> future Trino SQL queries.

## Notes

The goal is not only to build the project, but to understand how each platform component works in practice.
