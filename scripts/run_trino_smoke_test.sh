#!/usr/bin/env bash
set -euo pipefail

docker exec -i lakehouse-trino trino < scripts/sql/trino_iceberg_smoke_test.sql
