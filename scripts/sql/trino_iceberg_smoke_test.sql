SHOW CATALOGS;

SHOW SCHEMAS FROM iceberg;

CREATE SCHEMA IF NOT EXISTS iceberg.bronze
WITH (location = 's3://warehouse/bronze');

CREATE TABLE IF NOT EXISTS iceberg.bronze.platform_smoke_test (
    id INTEGER,
    message VARCHAR,
    created_at TIMESTAMP
)
WITH (
    format = 'PARQUET'
);

INSERT INTO iceberg.bronze.platform_smoke_test
VALUES
    (1, 'trino can write to iceberg on minio', current_timestamp);

SELECT *
FROM iceberg.bronze.platform_smoke_test;

SELECT *
FROM iceberg.bronze."platform_smoke_test$files";

SELECT *
FROM iceberg.bronze."platform_smoke_test$history";
