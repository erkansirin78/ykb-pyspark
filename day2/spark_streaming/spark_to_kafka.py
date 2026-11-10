from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder
        .appName("Read From Kafka")
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.3")
.getOrCreate())


spark.sparkContext.setLogLevel('ERROR')


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:29092") \
  .option("subscribe", "test1") \
.option("startingOffsets", "earliest") \
  .load()


df_deser = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

checkpointDir = "hdfs://namenode:9000/tmp/kafka_stream_demo2"

# query = (df_deser.writeStream.format("console").outputMode("append")
# .trigger(processingTime="10 second")
# .option("checkpointLocation", checkpointDir)
# .option("numRows",20)
# .option("truncate",False)
#  .start()       )

query = df_deser.writeStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:29092") \
  .option("topic", "test2") \
    .option("checkpointLocation", checkpointDir) \
  .start()

query.awaitTermination()