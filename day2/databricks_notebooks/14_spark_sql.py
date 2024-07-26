# Databricks notebook source
df = spark.read.format("csv") \
.option("header", True) \
.option("inferSchema", True) \
.option("sep", ",") \
.load("file:///databricks/driver/Churn_Modelling.csv")

# COMMAND ----------

! wget -O Churn_Modelling.csv \
https://github.com/erkansirin78/datasets/raw/master/Churn_Modelling.csv

# COMMAND ----------

df.createTempView("churn")

# COMMAND ----------

spark.sql("""
          
          select * from churn limit 5
          
          """).toPandas()

# COMMAND ----------

special_country = "France"
age_gt_40 = 40

# COMMAND ----------

df4 = spark.sql(f"""
          
          select * from churn where Geography = '{special_country}' AND Age > '{age_gt_40}'
          
          """)

# COMMAND ----------

df4.limit(5).toPandas()

# COMMAND ----------

df4.write.format("csv").option("header", True).option("sep", ";") \
    .save("file:///databricks/driver/churn_france_gt_40_csv")

# COMMAND ----------

! ls -l churn_france_gt_40_csv

# COMMAND ----------

! head churn_france_gt_40_csv/part-00000-tid-3318182008736482289-a10877bf-8e4d-4daa-bf0d-4eb53d70210a-156-1-c000.csv

# COMMAND ----------

df4.write.format("parquet").mode("overwrite") \
    .save("file:///databricks/driver/churn_france_gt_40_parquet")

# COMMAND ----------


