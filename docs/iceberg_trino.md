# Iceberg and Trino Local Setup

## Goal

Add a local open lakehouse query layer using:

- MinIO as local object storage
- Apache Iceberg as the table format
- Iceberg REST Catalog as the catalog service
- Trino as the distributed SQL query engine

## Mental model

In Snowflake, storage, metadata, transactions and compute are bundled inside the platform.

In this local lakehouse setup, those responsibilities are separated:

- MinIO stores the physical files.
- Iceberg defines table metadata, snapshots, schema and file tracking.
- Iceberg REST Catalog exposes table metadata to engines.
- Trino executes SQL queries against Iceberg tables.

## Naming model

Trino uses:

catalog.schema.table

For example:

iceberg.bronze.platform_smoke_test

Where:

- iceberg = Trino catalog
- bronze = Iceberg namespace/schema
- platform_smoke_test = Iceberg table

## Why Iceberg matters

Without Iceberg, the lake would mostly be a collection of files.

With Iceberg, the lake gets table-level behavior:

- schema tracking
- metadata files
- snapshots
- time travel foundation
- hidden file tracking
- safer table evolution
- metadata tables such as $files and $history

## Current limitation

The current setup is for local learning and smoke testing. It is not production-grade yet.

Future improvements:

- persist catalog metadata more explicitly
- add Spark Structured Streaming writer
- add compaction jobs
- add dbt models on top of Trino
- add data quality checks
