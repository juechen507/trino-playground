from pyspark.sql import SparkSession

# ====================== Spark 构建 ======================
spark = SparkSession.builder \
    .appName("Kafka-To-Iceberg-S3") \
    .master("spark://spark:7077") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog") \
#    .config("spark.sql.catalog.iceberg.type", "hadoop") \
    .config("spark.sql.catalog.iceberg.type", "hive") \
    .config("spark.sql.catalog.iceberg.warehouse", "s3://datalake/warehouse") \
    .config("spark.hadoop.fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.sql.adaptive.enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ====================== 读取 Kafka ======================
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "test") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# ====================== 转换字段 ======================
result_df = df.selectExpr(
    "CAST(key AS STRING)",
    "CAST(value AS STRING)",
    "partition",
    "offset",
    "timestamp"
)

# ====================== 写入 Iceberg ======================
query = result_df.writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://datalake/warehouse/checkpoint/kafka2demo") \
    .trigger(processingTime="10 seconds") \
    .toTable("iceberg.demo.spark_kafka_to_iceberg") 

query.awaitTermination()
