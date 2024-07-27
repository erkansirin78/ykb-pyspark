# Databricks notebook source
! wget -O Advertising.csv  https://raw.githubusercontent.com/erkansirin78/datasets/master/Advertising.csv

# COMMAND ----------

! head Advertising.csv

# COMMAND ----------

df = spark.read.format("csv") \
.option("header",True) \
.option("inferSchema",True) \
.option("sep",",") \
.load("file:///databricks/driver/Mall_Customers.csv")

# COMMAND ----------

df.limit(5).toPandas()

# COMMAND ----------

# id'yi almazdım
# Veri keşfi
# Veri temizlik ve hazırlığı
# kategorik değişkenleri hazırla ohe
# standardizasyon
# modeli eğit
# modeli test et

# COMMAND ----------

# Kategorik değişken işleme hazırlığı: StringIndexer
from pyspark.ml.feature import StringIndexer

# COMMAND ----------

gender_stridx_obj = StringIndexer(inputCol="Gender", 
                                  outputCol="genderIdx", 
                                  handleInvalid='error')

# COMMAND ----------

df1 = gender_stridx_obj.fit(df).transform(df)

# COMMAND ----------

df1.limit(5).toPandas()

# COMMAND ----------

# OneHotEncoder
from pyspark.ml.feature import OneHotEncoder

# COMMAND ----------

ohe_obj = OneHotEncoder(inputCols=["genderIdx"],
    outputCols=["OHE_Cols"],
    handleInvalid='error')

# COMMAND ----------

df2 = ohe_obj.fit(df1).transform(df1)

# COMMAND ----------

df2.limit(5).toPandas()

# COMMAND ----------

df2.printSchema()

# COMMAND ----------

# Tüm inputları bir sütunda vektör olarak topla
# VectorAssembler
from pyspark.ml.feature import VectorAssembler

# COMMAND ----------

assembler_obj = VectorAssembler(inputCols=['Age','AnnualIncome','OHE_Cols'], 
                                outputCol='vector_assebmled_cols', 
                                handleInvalid='skip')

# COMMAND ----------

df3 = assembler_obj.transform(df2)

# COMMAND ----------

df3.limit(5).toPandas()

# COMMAND ----------

df3.printSchema()

# COMMAND ----------

# Standardizasyon
from pyspark.ml.feature import StandardScaler

# COMMAND ----------

scaler = StandardScaler(withMean=False, 
                        withStd=True, 
                        inputCol='vector_assebmled_cols', 
                        outputCol='features')

# COMMAND ----------

df4 = scaler.fit(df3).transform(df3)

# COMMAND ----------

df4.limit(5).toPandas()

# COMMAND ----------

df5 = df4.withColumnRenamed("SpendingScore", "label")

# COMMAND ----------

df5.limit(5).toPandas()

# COMMAND ----------

# Split data for test and train
df_train, df_test = df5.randomSplit([0.8, 0.2], seed=142)

# COMMAND ----------

print(df_train.count())
print(df_test.count())

# COMMAND ----------

# Model
from pyspark.ml.regression import DecisionTreeRegressor

# COMMAND ----------

estimator = DecisionTreeRegressor(maxBins=28, labelCol="label", featuresCol="features")

# COMMAND ----------

gbt_model = estimator.fit(df_train)

# COMMAND ----------

# test the model
transformed_df = gbt_model.transform(df_test)

# COMMAND ----------

transformed_df.limit(5).toPandas()

# COMMAND ----------

# Evaluate the model
from pyspark.ml.evaluation import RegressionEvaluator

# COMMAND ----------

evaluator = RegressionEvaluator()

# COMMAND ----------

mae = evaluator.evaluate(transformed_df, {evaluator.metricName: "mae"})
r2 = evaluator.evaluate(transformed_df, {evaluator.metricName: "r2"})

# COMMAND ----------

print(r2)
print(mae)

# COMMAND ----------


