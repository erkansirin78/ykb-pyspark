# `spark-history` — Spark History Server

`spark:4.1.3-java21-python3`. Reads Spark event logs from `hdfs:///spark-logs` and serves the post-mortem UI on `18080` (DAGs, stages, SQL, executor timeline) for finished jobs submitted from [`spark-client`](12_spark-client.md).

## Compose service
```yaml
spark-history:
  image: spark:4.1.3-java21-python3
  depends_on: [ namenode ]
  restart: unless-stopped
  environment:
    HADOOP_CONF_DIR: /opt/hadoop-conf
    SPARK_NO_DAEMONIZE: "true"
  volumes:
    - ./conf/hadoop:/opt/hadoop-conf:ro
    - ./conf/spark/spark-defaults.conf:/opt/spark/conf/spark-defaults.conf:ro
  ports: [ "18080:18080" ]
  command: >
    /opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer
```

Reads the same `spark.eventLog.dir` that `spark-client` writes to (`hdfs:///spark-logs`, created by the [`namenode`](02_namenode.md) bootstrap with `1777`).

| | |
|---|---|
| History UI | http://localhost:18080 |

## Examples
```bash
# generate an event log, then refresh http://localhost:18080
docker exec spark-client /opt/spark/bin/spark-submit \
  --master yarn --deploy-mode client --conf spark.driver.host=spark-client \
  --class org.apache.spark.examples.SparkPi \
  /opt/spark/examples/jars/spark-examples_2.13-4.1.3.jar 5

# what event logs exist
docker exec namenode hdfs dfs -ls /spark-logs

# history server health
docker logs --tail 20 spark-history
curl -sI http://localhost:18080 | head -1
```

Empty UI ("No completed applications") just means no Spark job has run yet. `/spark-logs` itself is created (mode `1777`) by the one-shot [`hdfs-init`](04_hdfs-init.md), which `spark-history` waits on (`condition: service_completed_successfully`) — so a missing-dir startup failure shouldn't happen.
