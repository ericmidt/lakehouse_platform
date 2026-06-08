from pyspark.sql import SparkSession


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("spark-iceberg-smoke-test")
        .getOrCreate()
    )

    spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.bronze")

    spark.sql("""
        CREATE TABLE IF NOT EXISTS iceberg.bronze.spark_smoke_test (
            id INT,
            message STRING
        )
        USING iceberg
    """)

    spark.sql("""
        INSERT INTO iceberg.bronze.spark_smoke_test
        VALUES (1, 'spark can write to iceberg')
    """)

    spark.sql("""
        SELECT *
        FROM iceberg.bronze.spark_smoke_test
    """).show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
