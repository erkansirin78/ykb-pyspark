# Databricks notebook source
! curl -o Mall_Customers.csv \
https://raw.githubusercontent.com/erkansirin78/datasets/master/Mall_Customers.csv

# COMMAND ----------

! head Mall_Customers.csv

# COMMAND ----------

df = (spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("sep", ",")
    .load("file:///databricks/driver/Mall_Customers.csv"))

# COMMAND ----------

df.show(5)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df_pd = df.limit(5).toPandas()

# COMMAND ----------

df_pd.head()

# COMMAND ----------


