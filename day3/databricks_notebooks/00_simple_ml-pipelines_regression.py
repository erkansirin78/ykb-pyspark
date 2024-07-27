# Databricks notebook source
df = spark.read.format("csv") \
.option("header",True) \
.option("inferSchema",True) \
.option("sep",",") \
.load("file:///databricks/driver/Mall_Customers.csv") \
.withColumnRenamed("SpendingScore", "label")

# COMMAND ----------

df.limit(5).toPandas()

# COMMAND ----------

from pyspark.ml.feature import StringIndexer
gender_stridx_obj = StringIndexer(inputCol="Gender", 
                                  outputCol="genderIdx", 
                                  handleInvalid='error')

# COMMAND ----------

from pyspark.ml.feature import OneHotEncoder
ohe_obj = OneHotEncoder(inputCols=["genderIdx"],
    outputCols=["OHE_Cols"],
    handleInvalid='error')

# COMMAND ----------

from pyspark.ml.feature import VectorAssembler
assembler_obj = VectorAssembler(inputCols=['Age','AnnualIncome','OHE_Cols'], 
                                outputCol='vector_assebmled_cols', 
                                handleInvalid='skip')

# COMMAND ----------

from pyspark.ml.feature import StandardScaler
scaler = StandardScaler(withMean=False, 
                        withStd=True, 
                        inputCol='vector_assebmled_cols', 
                        outputCol='features')

# COMMAND ----------

df_train, df_test = df.randomSplit([0.8, 0.2], seed=142)

# COMMAND ----------

from pyspark.ml.regression import DecisionTreeRegressor
estimator = DecisionTreeRegressor()

# COMMAND ----------

from pyspark.ml.pipeline import Pipeline, PipelineModel

# COMMAND ----------

pipeline_obj = Pipeline().setStages([gender_stridx_obj, ohe_obj, assembler_obj, scaler, estimator])

# COMMAND ----------

pipeline_model = pipeline_obj.fit(df_train)

# COMMAND ----------

transformed_df = pipeline_model.transform(df_test)

# COMMAND ----------

transformed_df.limit(5).toPandas()

# COMMAND ----------

pipeline_model.stages

# COMMAND ----------

from pyspark.ml.evaluation import RegressionEvaluator

# COMMAND ----------

evaluator = RegressionEvaluator(metricName='r2')

# COMMAND ----------

r2 = evaluator.evaluate(transformed_df)

# COMMAND ----------

r2

# COMMAND ----------

pipeline_model.write().overwrite().save("file:///databricks/driver/simple_ml_pipeline")

# COMMAND ----------

pipeline_model_loaded = PipelineModel.load("file:///databricks/driver/simple_ml_pipeline")

# COMMAND ----------

! ls -l

# COMMAND ----------

pipeline_model_loaded.transform(df_test).limit(5).toPandas()

# COMMAND ----------

pipeline_model_loaded.transform(df).limit(5).toPandas()

# COMMAND ----------


