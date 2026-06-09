CREATE SCHEMA IF NOT EXISTS iceberg.silver
WITH (location = 's3://warehouse/silver');

DROP TABLE IF EXISTS iceberg.silver.order_submitted_events;

CREATE TABLE iceberg.silver.order_submitted_events
WITH (
    format = 'PARQUET'
) AS
SELECT
    json_extract_scalar(raw_payload, '$.event_id') AS event_id,
    json_extract_scalar(raw_payload, '$.event_type') AS event_type,
    from_iso8601_timestamp(json_extract_scalar(raw_payload, '$.event_time')) AS event_time,
    CAST(json_extract_scalar(raw_payload, '$.schema_version') AS INTEGER) AS schema_version,
    json_extract_scalar(raw_payload, '$.account_id') AS account_id,
    json_extract_scalar(raw_payload, '$.order_id') AS order_id,
    json_extract_scalar(raw_payload, '$.symbol') AS symbol,
    json_extract_scalar(raw_payload, '$.side') AS side,
    CAST(json_extract_scalar(raw_payload, '$.quantity') AS INTEGER) AS quantity,
    json_extract_scalar(raw_payload, '$.order_type') AS order_type,
    json_extract_scalar(raw_payload, '$.status') AS status,
    json_extract_scalar(raw_payload, '$.source') AS source,

    source_topic,
    source_partition,
    source_offset,
    source_timestamp,
    ingestion_timestamp,
    message_key,
    raw_payload
FROM iceberg.bronze.order_submitted_events
WHERE raw_payload IS NOT NULL;
