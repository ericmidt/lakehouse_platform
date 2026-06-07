#!/usr/bin/env bash
set -euo pipefail

docker exec lakehouse-redpanda rpk topic create order_submitted || true
docker exec lakehouse-redpanda rpk topic create order_filled || true
docker exec lakehouse-redpanda rpk topic create trade_executed || true
docker exec lakehouse-redpanda rpk topic create api_request_log || true

docker exec lakehouse-redpanda rpk topic list
