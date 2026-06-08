from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("read-kafka-orders-console")
        .getOrCreate()
    )

    orders = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "redpanda:9092")
        .option("subscribe", "order_submitted")
        .option("startingOffsets", "earliest")
        .load()
    )

    readable_orders = orders.select(
        col("topic"),
        col("partition"),
        col("offset"),
        col("timestamp"),
        col("key").cast("string").alias("message_key"),
        col("value").cast("string").alias("message_value"),
    )

    query = (
        readable_orders.writeStream
        .format("console")
        .outputMode("append")
        .option("truncate", "false")
        .start()
    )

    query.awaitTermination(30)
    query.stop()
    spark.stop()


if __name__ == "__main__":
    main()
