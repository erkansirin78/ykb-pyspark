# `spark-client` — Spark-on-YARN submission box

`spark:4.1.3-java21-python3`. An idle container (`sleep infinity`) you `docker exec` into to run `spark-submit` / `spark-sql` / `pyspark` / `spark-shell` against [`resourcemanager`](05_resourcemanager.md), writing through the shared [`hive-metastore`](09_hive-metastore.md). Live driver UI on `4040` while a job runs.

## Compose service
```yaml
spark-client:
  image: spark:4.1.3-java21-python3
  depends_on: [ resourcemanager, hive-metastore ]
  environment:
    HADOOP_CONF_DIR: /opt/hadoop-conf
    HOME: /tmp
    _JAVA_OPTIONS: "-Duser.home=/tmp"
  volumes:
    - ./conf/hadoop:/opt/hadoop-conf:ro
    - ./conf/spark/spark-defaults.conf:/opt/spark/conf/spark-defaults.conf:ro
    - ./conf/hive/hive-site.xml:/opt/spark/conf/hive-site.xml:ro
  command: sleep infinity
  ports: [ "4040:4040" ]
```

Notes baked in:
- `spark-defaults.conf` pins `spark.sql.hive.metastore.version=4.0.1` + `spark.sql.hive.metastore.jars=maven` (Spark 4.1.3 ships Hive 2.3.10 client jars; would call `get_table` on a Hive 4 metastore). First run downloads them via Maven (~300 MB, cached at `/tmp/.ivy2`).
- `_JAVA_OPTIONS=-Duser.home=/tmp` because the image's `spark` user has `HOME=/nonexistent`, which Ivy reads for its cache.

| | |
|---|---|
| Live driver UI | http://localhost:4040 (only during a job) |
| History (post-mortem) | http://localhost:18080 → [`spark-history`](11_spark-history.md) |

## Examples
```bash
# SparkPi on YARN
docker exec spark-client /opt/spark/bin/spark-submit \
  --master yarn --deploy-mode client --conf spark.driver.host=spark-client \
  --class org.apache.spark.examples.SparkPi \
  /opt/spark/examples/jars/spark-examples_2.13-4.1.3.jar 5

# Spark SQL writing to the Hive metastore on YARN
docker exec spark-client /opt/spark/bin/spark-sql \
  --master yarn --conf spark.driver.host=spark-client -e "
    CREATE DATABASE IF NOT EXISTS demo;
    USE demo;
    CREATE TABLE IF NOT EXISTS hello_spark(id INT, msg STRING) USING PARQUET;
    INSERT INTO hello_spark VALUES (1,'spark'),(2,'on'),(3,'yarn');
    SELECT * FROM hello_spark ORDER BY id;
  "

# PySpark: HDFS CSV -> ORC Hive table (the notebook flow, as a script)
docker exec namenode bash -c \
  "curl -sO https://raw.githubusercontent.com/erkansirin78/datasets/master/Advertising.csv && \
   hdfs dfs -mkdir -p /user/root && hdfs dfs -put -f Advertising.csv /user/root/"

docker exec spark-client /opt/spark/bin/spark-submit --master yarn \
  --conf spark.driver.host=spark-client /dev/stdin <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Spark YARN Example").enableHiveSupport().getOrCreate()
df = (spark.read.format("csv").option("header", True).option("inferSchema", True)
      .load("hdfs://namenode:9000/user/root/Advertising.csv"))
df = df.toDF(*[c.lower() for c in df.columns])
df.write.mode("overwrite").format("orc").saveAsTable("test1.spark_adv_orc")
spark.table("test1.spark_adv_orc").show(4)
spark.stop()
PY

# interactive
docker exec -it spark-client /opt/spark/bin/pyspark --master yarn --conf spark.driver.host=spark-client
```

Spark writes are visible to [`hiveserver2`](10_hiveserver2.md)/Hue (shared catalog); Spark does **not** use Tez — that's only Hive's engine.
