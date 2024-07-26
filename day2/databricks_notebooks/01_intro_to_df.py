# Databricks notebook source
spark.version

# COMMAND ----------

df = spark.createDataFrame([('Suha', 28), ('Murat', 42), ('Bengisu', 29), ('Tuba', 33)]
                           , ['name', 'age'])

# COMMAND ----------

df.show()

# COMMAND ----------

df.printSchema()

# COMMAND ----------


