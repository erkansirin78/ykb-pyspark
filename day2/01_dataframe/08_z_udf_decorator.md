- https://justinmatters.co.uk/wp/using-the-pyspark-udf-decorator-with-currying/
## Create udf
```python
from pyspark.sql import functions as fn
 
def multiply_by_two(number):
    return number * 2
 
udf_multiply_by_two = fn.udf(multiply_by_two, T.IntegerType())
 
display(df.withColumn(
    "times_two", udf_multiply_by_two("integers")
))
```

## Using the @udf Decorator
```python
@udf(T.IntegerType())
def decorator_multiply_by_three(number):
    return number * 3
 
display(df.withColumn(
    "decorator_times_three", decorator_multiply_by_three("integers")
))
```