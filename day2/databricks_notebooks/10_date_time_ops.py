# Databricks notebook source
! wget -O Fire_Incidents.csv.gz \
https://github.com/erkansirin78/datasets/raw/master/Fire_Incidents.csv.gz

# COMMAND ----------

df = spark.read \
.format("csv") \
.option("header", True) \
.option("inferSchema", True) \
.option("compression","gzip") \
.load("file:///databricks/driver/Fire_Incidents.csv.gz")

# COMMAND ----------

df.limit(1).toPandas()

# COMMAND ----------

ts_cols = ['Incident Date','Alarm DtTm']

# COMMAND ----------

df.select(ts_cols).show(n=4, truncate=False)

# COMMAND ----------

df2 = df.select(ts_cols)

# COMMAND ----------

df2.show(2)

# COMMAND ----------

df2.printSchema()

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

df3 = df2.withColumn("Alarm_DtTm_New", 
                    F.to_timestamp(F.col("Alarm DtTm"), 'MM/dd/yyyy hh:mm:ss a'))

# COMMAND ----------

df3.show(n=4, truncate=False)

# COMMAND ----------

df3.printSchema()

# COMMAND ----------

df4 = df3.withColumn("Incident_Date", 
                     F.to_date(F.col("Incident Date"), 'MM/dd/yyyy'))
df4.limit(3).toPandas()

# COMMAND ----------

df5 = df4.withColumn("Incident_Date_Str", 
                     F.date_format(F.col("Incident_Date"), 'yyyyMM'))


df5.limit(3).toPandas()

# COMMAND ----------

df6 = df5.withColumn("prev_month", F.add_months("Incident_Date", -1)) \
    .withColumn("last_day", F.last_day("Incident_date")) \
        .withColumn("prev_month_ed", F.last_day("prev_month"))

# COMMAND ----------

df6.limit(3).toPandas()

# COMMAND ----------


