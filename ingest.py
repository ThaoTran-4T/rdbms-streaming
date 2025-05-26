from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType
from pyspark.sql.functions import from_json, col

# os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-11.0.17"
os.environ["SPARK_CONF_DIR"] = "G:/DEMO/KafkaDemo/conf"
os.environ['PYSPARK_PYTHON'] = "G:/DEMO/KafkaDemo/venv/Scripts/python.exe"


    
spark = SparkSession.builder \
        .appName("ingest") \
        .getOrCreate()

inventoryFields = [
    StructField("inventoryId", IntegerType()),             # inventory_id
    StructField("productId", IntegerType()),               # product_id
    StructField("warehouseLocation", StringType()),        # warehouse_location
    StructField("quantityAvailable", IntegerType()),       # quantity_available
    StructField("restockDate", DateType())                 # restock_date
]

schema = StructType([
    StructField("payload", StructType([
        StructField("before", StructType(inventoryFields)),
        StructField("after", StructType(inventoryFields)),
        StructField("ts_ms", StringType()),
        StructField("op", StringType())
    ]))
])

spark.sql("""CREATE SCHEMA IF NOT EXISTS local.inventory_schema""")
spark.sql("""
          CREATE TABLE IF NOT EXISTS local.inventory_schema.inventory_logs
          (
              inventoryId INT,
              productId INT,
              warehouseLocation STRING,
              quantityAvailable INT,
              restockDate DATE
          ) 
          USING iceberg
          """)

lines = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "inventory.public.inventory") \
  .load()

lines2 = lines.selectExpr("CAST(value AS STRING)")
parsedData = lines2.select(from_json(col("value"), schema).alias("data"))

# Flatten the data and select fields
flattenedData = parsedData.select(
    col("data.payload.after.*")
).filter(col("data.payload.op").isin("c"))  # Filter for create, update, delete operations

checkpoint_dir = "s3a://inventorylog.checkpoint"

# Define MinIO (S3) output path
minio_output_path = "s3a://inventorylogs/"

# Write the streaming output to MinIO
streamingQuery = flattenedData \
    .writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .option("path", minio_output_path) \
    .option("checkpointLocation", checkpoint_dir) \
    .start()

# Start streaming
streamingQuery.awaitTermination()