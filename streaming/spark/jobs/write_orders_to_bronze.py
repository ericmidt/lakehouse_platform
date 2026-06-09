from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("write-orders-to-bronze")
        .getOrCreate()
    )

    spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.bronze")

    spark.sql("""
        CREATE TABLE IF NOT EXISTS iceberg.bronze.order_submitted_events (
            source_topic STRING,
            source_partition INT,
            source_offset BIGINT,
            source_timestamp TIMESTAMP,
            ingestion_timestamp TIMESTAMP,
            message_key STRING,
            raw_payload STRING
        )
        USING iceberg
    """)

    kafka_orders = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "redpanda:9092")
        .option("subscribe", "order_submitted")
        .option("startingOffsets", "earliest")
        .load()
    )

    bronze_orders = kafka_orders.select(
        col("topic").alias("source_topic"),
        col("partition").alias("source_partition"),
        col("offset").alias("source_offset"),
        col("timestamp").alias("source_timestamp"),
        current_timestamp().alias("ingestion_timestamp"),
        col("key").cast("string").alias("message_key"),
        col("value").cast("string").alias("raw_payload"),
    )

    query = (
        bronze_orders.writeStream
        .format("iceberg")
        .outputMode("append")
        .option("checkpointLocation", "/home/iceberg/checkpoints/order_submitted_events")
        .trigger(availableNow=True)
        .toTable("iceberg.bronze.order_submitted_events")
    )

    query.awaitTermination()

    spark.stop()


if __name__ == "__main__":
    main()
