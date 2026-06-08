#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker-compose.yml -f docker-compose.spark.yml up -d

docker exec lakehouse-spark spark-submit \
  --properties-file /home/iceberg/conf/spark-defaults.conf \
  /home/iceberg/jobs/spark_iceberg_smoke_test.py

docker exec lakehouse-trino trino --execute \
"SELECT * FROM iceberg.bronze.spark_smoke_test"
