# Submit format
```
spark-submit \
  --class <main-class> \
  --master <master-url> \
  --deploy-mode <deploy-mode> \
  --conf <key>=<value> \
  ... # other options
  <application-jar> or <apllication.py> \
  [application-arguments]
```

## -
` Let's submit a simple Spark application that read data and print 20 rows to screen. `  


# Simple submit
```
 spark-submit --master local \
 simple_submit.py \
 -i file:///opt/examples/datasets/Churn_Modelling.csv \
 -sch True \
 -head True
```

# Submit with configuration
```
(venvspark) [train@localhost 05_submit_spark_applications]$ spark-submit \
    --master yarn \
    --deploy-mode client \
    --num-executors 2 \
    --conf spark.sql.autoBroadcastJoinThreshold=-1 \
    simple_submit.py \
    -i file:///home/train/datasets/market5mil_parquet \
    -f parquet \
    -c snappy \
    -name SparkApplicationSubmit
```

# Submit with extra packages
```
(venvspark) [train@localhost 05_submit_spark_applications]$ spark-submit \
    --master yarn \
    --deploy-mode client \
    --num-executors 2 \
    --packages "org.apache.spark:spark-avro_2.12:3.0.0" \
    --conf spark.sql.autoBroadcastJoinThreshold=-1 \
    simple_submit.py \
    -i hdfs://localhost:9000/user/train/datasets/market5mil_parquet \
    -f parquet \
    -c snappy \
    --appName SparkApplicationSubmit
```

# After submit you see the following logs
```
:: resolving dependencies :: org.apache.spark#spark-submit-parent-630b8af2-4eaf-4f64-a2de-15b84345333e;1.0
        confs: [default]
        found org.apache.spark#spark-avro_2.12;3.0.0 in central
        found org.spark-project.spark#unused;1.0.0 in central
:: resolution report :: resolve 950ms :: artifacts dl 22ms
        :: modules in use:
        org.apache.spark#spark-avro_2.12;3.0.0 from central in [default]
        org.spark-project.spark#unused;1.0.0 from central in [default]
        ---------------------------------------------------------------------
        |                  |            modules            ||   artifacts   |
        |       conf       | number| search|dwnlded|evicted|| number|dwnlded|
        ---------------------------------------------------------------------
        |      default     |   2   |   0   |   0   |   0   ||   2   |   0   |
        ---------------------------------------------------------------------
:: retrieving :: org.apache.spark#spark-submit-parent-630b8af2-4eaf-4f64-a2de-15b84345333e
        confs: [default]
```

# Submit with extra jars
```
(venvspark) [train@localhost 05_submit_spark_applications]$ spark-submit \
        --master yarn \
        --deploy-mode client \
        --num-executors 2 \
        --jars "hdfs://localhost:9000/tmp/extra-jars/org.apache.spark_spark-avro_2.12-3.0.0.jar" \
        --conf spark.sql.autoBroadcastJoinThreshold=-1 \
        simple_submit.py \
        -i hdfs://localhost:9000/user/train/datasets/market5mil_parquet \
        -f parquet \
        -c snappy \
        --appName SparkApplicationSubmit
```
## Note
```
--jars.

Spark uses the following URL scheme to allow different strategies for disseminating jars:

file: - Absolute paths and file:/ URIs are served by the driver’s HTTP file server, and every executor pulls the file from the driver HTTP server.
hdfs:, http:, https:, ftp: - these pull down files and JARs from the URI as expected
local: - a URI starting with local:/ is expected to exist as a local file on each worker node. This means that no network IO will be incurred, and works well for large files/JARs that are pushed to each worker, or shared via NFS, GlusterFS, etc.

```