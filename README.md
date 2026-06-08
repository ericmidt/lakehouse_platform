# Lakehouse Platform

A hands-on data platform engineering project for learning open lakehouse technologies in practice.

The goal is to build a local-first brokerage-style data platform that ingests event streams, stores them in an Apache Iceberg lakehouse, exposes them through Trino, transforms them with dbt, orchestrates workloads with Airflow, and later evolves toward Kubernetes and GCP.

This project is intentionally incremental. Each phase introduces one or two new concepts at a time.

## Why this project exists

My current strongest areas are:

- SQL
- dbt
- Snowflake
- Airflow
- Python

This project is meant to deepen practical understanding of:

- Kafka-compatible event streaming
- Spark Structured Streaming
- Apache Iceberg
- Trino
- object storage
- open lakehouse architecture
- Docker-based local development
- Kubernetes and Helm
- Terraform
- GCP data services

The long-term goal is to become stronger in data platform engineering, not just analytics engineering or warehouse-based data engineering.

## Target architecture

```text
Synthetic brokerage event generator
        |
        v
Redpanda / Kafka-compatible broker
        |
        v
Spark Structured Streaming
        |
        v
Apache Iceberg tables
        |
        v
MinIO object storage
        |
        v
Trino SQL query engine
        |
        v
dbt models
        |
        v
Gold data marts, quality checks, and BI-ready datasets
```

Future cloud version:

```text
Kafka / Pub/Sub / Datastream
        |
        v
Dataproc / Serverless Spark
        |
        v
Apache Iceberg on GCS
        |
        v
Trino on Kubernetes
        |
        v
dbt + Airflow / Composer
        |
        v
BI, reverse ETL, monitoring, and alerting
```

## Business domain

The project simulates a brokerage / trading platform.

Example event types:

- account_created
- account_updated
- order_submitted
- order_filled
- trade_executed
- position_updated
- funding_event
- api_request_log

Example business questions:

- Which accounts submit the most orders?
- Which symbols have the highest trade volume?
- Which API endpoints have the highest p95 latency?
- Which orders were submitted but never filled?
- Which events arrived late, duplicated, or malformed?
- How fresh is the bronze/silver/gold data?

## Current status

Implemented or in progress:

- Local repository structure
- Docker-based local environment
- Redpanda as a Kafka-compatible broker
- Redpanda Console for local inspection
- MinIO as local object storage
- Iceberg REST Catalog
- Trino with Iceberg catalog configuration
- Trino smoke test for creating and querying Iceberg tables
- Spark runtime container
- Spark configuration for Iceberg REST Catalog and MinIO
- Initial Spark Iceberg smoke test job

Next immediate goal:

```text
Validate that Spark can write an Iceberg table and that Trino can query it.
```

## Repository structure

```text
.
├── apps/
│   └── event-generator/
│       └── src/
├── airflow/
│   └── dags/
├── dbt/
│   └── lakehouse_platform/
├── docs/
├── infra/
│   └── docker/
│       └── trino/
│           └── catalog/
├── scripts/
├── streaming/
│   └── spark/
│       ├── conf/
│       ├── jobs/
│       └── checkpoints/
├── docker-compose.yml
├── docker-compose.spark.yml
└── README.md
```

## Local development environment

This project is developed on:

- Windows 11
- WSL
- Docker Desktop
- Docker Compose

Recommended location inside WSL:

```bash
~/projects/lakehouse_platform
```

Avoid working from `/mnt/c/...` when possible because Linux tooling is usually faster and smoother when files are stored directly inside the WSL filesystem.

## Running the local stack

Start the base stack:

```bash
docker compose up -d
```

Start the base stack plus Spark:

```bash
docker compose -f docker-compose.yml -f docker-compose.spark.yml up -d
```

Check running containers:

```bash
docker ps
```

Useful local UIs:

```text
Redpanda Console: http://localhost:8080
MinIO Console:    http://localhost:9001
Trino:            localhost:8081
```

Default MinIO credentials:

```text
username: minioadmin
password: minioadmin
```

## Current smoke tests

Run the Trino and Iceberg smoke test:

```bash
./scripts/run_trino_smoke_test.sh
```

Run the Spark and Iceberg smoke test:

```bash
docker exec -it lakehouse-spark spark-submit \
  --properties-file /home/iceberg/conf/spark-defaults.conf \
  /home/iceberg/jobs/spark_iceberg_smoke_test.py
```

Then validate from Trino:

```bash
docker exec -it lakehouse-trino trino --execute \
"SELECT * FROM iceberg.bronze.spark_smoke_test"
```

## Learning notes

### Kafka / Redpanda

Kafka-style systems are append-only event logs.

Important concepts:

- topic
- partition
- offset
- producer
- consumer
- consumer group
- ordering within partitions
- replayability

In this project, Redpanda is used as a Kafka-compatible local broker.

### Object storage

Object storage is where lakehouse files live.

In production this could be:

- S3
- GCS
- ADLS

Locally this project uses:

- MinIO

### Apache Iceberg

Iceberg is the table format.

It gives table-like behavior on top of files:

- schemas
- snapshots
- metadata files
- manifest files
- table history
- safer schema evolution
- support for multiple engines

Without Iceberg, the lake is mostly a collection of files.

With Iceberg, the lake has table metadata and transaction-like behavior.

### Trino

Trino is the distributed SQL query engine.

In this project, Trino queries Iceberg tables stored on MinIO.

Naming pattern:

```text
catalog.schema.table
```

Example:

```text
iceberg.bronze.spark_smoke_test
```

### Spark

Spark is the processing engine.

In the current phase, Spark is being used to write a simple Iceberg table.

In the next phase, Spark Structured Streaming will read events from Redpanda/Kafka and write bronze Iceberg tables.

### dbt

dbt will be used after the bronze layer exists.

Planned pattern:

```text
bronze -> silver -> gold
```

Bronze:

- raw events
- ingestion metadata
- source topic
- source partition
- source offset
- raw payload

Silver:

- typed records
- deduplicated events
- validated schemas
- cleaned business entities

Gold:

- BI-ready marts
- business metrics
- platform health metrics

### Airflow

Airflow will orchestrate workloads.

It will not process the data directly.

Planned DAGs:

- generate synthetic events
- submit Spark streaming jobs
- run dbt models
- run data quality checks
- compact Iceberg tables
- publish reverse ETL outputs

## Roadmap

### Phase 1: Local broker and producer

Goal:

```text
Generate synthetic brokerage events and publish them to Redpanda.
```

Components:

- Redpanda
- Redpanda Console
- Python event generator

Status:

```text
In progress / partially implemented
```

### Phase 2: Object storage

Goal:

```text
Use MinIO as local object storage.
```

Components:

- MinIO
- warehouse bucket

Status:

```text
Implemented
```

### Phase 3: Iceberg and Trino

Goal:

```text
Create and query Iceberg tables through Trino.
```

Components:

- Iceberg REST Catalog
- Trino
- Iceberg catalog configuration
- smoke test SQL

Status:

```text
Implemented
```

### Phase 4: Spark runtime

Goal:

```text
Validate that Spark can write Iceberg tables and Trino can query them.
```

Components:

- Spark container
- Spark Iceberg configuration
- Spark smoke test job

Status:

```text
In progress
```

### Phase 5: Spark Structured Streaming bronze layer

Goal:

```text
Read Redpanda/Kafka events with Spark Structured Streaming and write bronze Iceberg tables.
```

Planned tables:

- iceberg.bronze.order_events
- iceberg.bronze.api_request_logs
- iceberg.bronze.trade_events

Key learning goals:

- readStream
- Kafka offsets
- checkpointing
- event-time vs processing-time
- raw payload preservation
- ingestion metadata
- streaming writes to Iceberg

### Phase 6: Silver and gold modeling with dbt

Goal:

```text
Transform raw Iceberg bronze tables into analytics-ready datasets.
```

Planned models:

- silver_orders
- silver_api_requests
- silver_trades
- gold_order_lifecycle
- gold_api_latency_daily
- gold_trade_volume_by_symbol
- gold_data_platform_health

Key learning goals:

- dbt with Trino
- incremental models
- tests
- documentation
- medallion modeling outside Snowflake

### Phase 7: Data quality and incident simulation

Goal:

```text
Simulate real production data problems and detect them.
```

Planned incidents:

- duplicate events
- malformed JSON
- missing required fields
- order_filled without order_submitted
- late arriving events
- stale topics

Key learning goals:

- quarantine tables
- reconciliation checks
- freshness checks
- event sequencing checks
- operational debugging

### Phase 8: Airflow orchestration

Goal:

```text
Use Airflow to orchestrate platform workloads.
```

Planned DAGs:

- start event generation
- run Spark jobs
- run dbt
- run quality checks
- generate health summaries

Key learning goals:

- orchestration vs processing
- retries
- task dependencies
- local DAG testing
- production-style operational flow

### Phase 9: Kubernetes and Helm

Goal:

```text
Move selected services/workloads toward a Kubernetes-style deployment model.
```

Planned components:

- local Kubernetes or kind
- Helm chart exploration
- Spark workload packaging
- Trino deployment pattern
- Airflow deployment pattern

Key learning goals:

- pods
- services
- deployments
- config maps
- secrets
- Helm values
- containerized data workloads

### Phase 10: Terraform and GCP

Goal:

```text
Design a cloud version of the platform on GCP.
```

Planned GCP equivalents:

- MinIO -> GCS
- local Spark -> Dataproc / Serverless Spark
- local Airflow -> Composer or Airflow on GKE
- local Postgres CDC -> Datastream
- local containers -> GKE / Artifact Registry

Key learning goals:

- infrastructure as code
- service accounts
- IAM
- GCS buckets
- GKE basics
- Dataproc basics
- cloud data platform trade-offs

## Git workflow

This project follows a company-style workflow:

```text
main
  -> feature branch
  -> small commits
  -> push branch
  -> pull request
  -> merge to main
```

Example:

```bash
git switch main
git pull origin main
git switch -c feature/add-spark-runtime
```

After each meaningful change:

```bash
git status --short
git add <changed-files>
git commit -m "Short descriptive message"
git push
```

After PR merge:

```bash
git switch main
git pull origin main
git branch -d <feature-branch>
```

## Design principles

- Prefer small, reviewable changes.
- Keep each branch focused.
- Commit after each meaningful file change.
- Document what each component does.
- Learn the mental model, not just the command.
- Build locally before moving to cloud.
- Avoid Kubernetes until the local data flow works.
- Avoid GCP until the local architecture is understood.
- Prefer debuggable steps over large jumps.

## Final target

By the end of the project, the platform should demonstrate:

- event streaming ingestion
- Spark Structured Streaming
- Apache Iceberg lakehouse tables
- object storage layout
- Trino SQL querying
- dbt transformation layer
- Airflow orchestration
- data quality and observability patterns
- Kubernetes deployment concepts
- Terraform and GCP architecture patterns
