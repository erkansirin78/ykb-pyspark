```
spark and sc are available
>>> from pyspark import SparkFiles
>>> github_url="https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv"
>>> sc.addFile(github_url)
>>> df = spark.read.csv(SparkFiles.get("Churn_Modelling.csv"),header= True, inferSchema=True)
>>> df.show()
```