# Databricks notebook source
! wget -O Hotel_Reviews.csv.gz \
https://github.com/erkansirin78/datasets/raw/master/Hotel_Reviews.csv.gz

# COMMAND ----------

df = (spark.read
.option("header", True)
.option("inferSchema", True)
.csv("file:///databricks/driver/Hotel_Reviews.csv.gz"))

# COMMAND ----------

df.count()

# COMMAND ----------

df.limit(1).toPandas()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.schema

# COMMAND ----------

from pyspark.sql.types import *

programmatical_schema = StructType([
        StructField("Hotel_Address",StringType(),True),
        StructField("Additional_Number_of_Scoring",IntegerType(),True),
        StructField("Review_Date",StringType(),True),
        StructField("Average_Score",FloatType(),True),
        StructField("Hotel_Name",StringType(),True),
        StructField("Reviewer_Nationality",StringType(),True),
        StructField("Negative_Review",StringType(),True),
        StructField("Review_Total_Negative_Word_Counts",IntegerType(),True),
        StructField("Total_Number_of_Reviews",IntegerType(),True),
        StructField("Positive_Review",StringType(),True),
        StructField("Review_Total_Positive_Word_Counts",IntegerType(),True),
        StructField("Total_Number_of_Reviews_Reviewer_Has_Given",IntegerType(),True),
        StructField("Reviewer_Score",FloatType(),True),
        StructField("Tags",StringType(),True),
        StructField("days_since_review",StringType(),True),
        StructField("lat",FloatType(),True),
        StructField("lng",FloatType(),True)
    ])

# COMMAND ----------

df2 = spark.read.option("header", True) \
.schema(programmatical_schema) \
.option("compression","gzip") \
.csv("file:///databricks/driver/Hotel_Reviews.csv.gz")

# COMMAND ----------

df2.printSchema()

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

df3 = df2.withColumn("Tags", 
                     F.split(F.col("Tags"), ",")
                     .cast( ArrayType(StringType())) )

# COMMAND ----------

df3.limit(1).toPandas()

# COMMAND ----------

df3.printSchema()

# COMMAND ----------

df3.filter("Average_Score < 6.0").limit(5).toPandas()

# COMMAND ----------

df3.filter(" TRIM(Reviewer_Nationality) == 'United Kingdom' ").limit(5).toPandas()

# COMMAND ----------

df3.filter(F.trim("Reviewer_Nationality") == 'United Kingdom').limit(5).toPandas()

# COMMAND ----------

df3.dtypes

# COMMAND ----------

str_cols = []
for i in df3.dtypes:
    if i[1] == 'string':
        str_cols.append(i[0])

# COMMAND ----------

str_cols

# COMMAND ----------

df4 = df3
for col in str_cols:
    df4 = df4.withColumn(col, F.trim(col))

# COMMAND ----------

for col in df4.columns:
    col_count = df4.filter( F.col(col).isNull() ).count()
    if ( col_count > 0):
        print("{} has {} null values.".format(col, col_count))


# COMMAND ----------


df5 = df4.withColumn("lat", F.when(F.col("lat").isNull(), 1000).otherwise(F.col("lat"))) \
    .withColumn("lng", F.when(F.col("lng").isNull(), 1000).otherwise(F.col("lng")))

# COMMAND ----------

for col in df5.columns:
    col_count = df5.filter( F.col(col).isNull() ).count()
    if ( col_count > 0):
        print("{} has {} null values.".format(col, col_count))

# COMMAND ----------

# udf

# COMMAND ----------

# MAGIC %md
# MAGIC UDF

# COMMAND ----------

def upper_case(x):
    return x.upper()

# COMMAND ----------

from pyspark.sql.types import StringType
upper_case_udf = F.udf(upper_case, StringType())

# COMMAND ----------

df5.withColumn("Nationality_Upper", upper_case_udf("Reviewer_Nationality")).select("Reviewer_Nationality","Nationality_Upper").show(4)

# COMMAND ----------

@udf(StringType())
def upper_case2(x):
    return x.upper()

df5.withColumn("Nationality_Upper", upper_case2("Reviewer_Nationality")).select("Reviewer_Nationality","Nationality_Upper").show(4)

# COMMAND ----------

@udf(IntegerType())
def decorator_multiply_by_three(number):
    return number * 3
 
display(df.withColumn(
    "decorator_times_three", decorator_multiply_by_three("integers")
))

# COMMAND ----------

df6 = df5.drop("Reviewer_Nationality")

# COMMAND ----------

df7 = df6.withColumnRenamed("Review_Total_Negative_Word_Counts","TN_Counts")

# COMMAND ----------


