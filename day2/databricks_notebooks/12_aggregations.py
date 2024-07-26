# Databricks notebook source
df = spark.read.option("header", True) \
.option("inderSchema", True) \
.option("compression","gzip") \
.csv("file:///databricks/driver/Hotel_Reviews.csv.gz")

# COMMAND ----------

from pyspark.sql.types import *

# COMMAND ----------

df2 = df.withColumn("Review_Date", F.to_date(F.col("Review_Date"),"M/d/yyyy"))

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

df3 = df2.select('Review_Date','Average_Score') \
    .withColumn("Year", F.year("Review_Date"))

df3.show(3)

# COMMAND ----------

df3.groupBy("Year").count().show()

# COMMAND ----------

df3.groupBy("Year").agg(F.avg("Average_Score").alias("Avg_Scr"), 
                        F.count("*").alias("count")) \
                            .orderBy(F.desc("count")) \
                            .show()

# COMMAND ----------


