# `hiveserver2` — JDBC SQL endpoint (on Tez)

`apache/hive:4.0.1`. The SQL front door: JDBC on `10000`, web UI on `10002`. Executes queries via **Tez** against the shared [`hive-metastore`](09_hive-metastore.md). Used by beeline, Hue's Hive editor, DBeaver, etc.

## Compose service
```yaml
hiveserver2:
  image: apache/hive:4.0.1
  depends_on: [ hive-metastore, tez ]
  environment:
    SERVICE_NAME: hiveserver2
    IS_RESUME: "true"
    HIVE_AUX_JARS_PATH: /opt/tez:/opt/tez/lib   # staged Tez client jars
  volumes:
    - ./conf/hive/hive-site.xml:/opt/hive/conf/hive-site.xml:ro
    - ./conf/tez/tez-site.xml:/opt/hive/conf/tez-site.xml:ro
    - ./jars/postgresql-42.7.4.jar:/opt/hive/lib/postgresql-42.7.4.jar:ro
    - tez-dist:/opt/tez:ro
  ports: [ "10000:10000", "10002:10002" ]
```

`hive-site.xml` sets `hive.execution.engine=tez`. The `tez-dist` volume is populated by the one-shot [`tez`](08_tez.md) service; HiveServer2 `depends_on` it with `condition: service_completed_successfully`, so it always starts with the Tez jars already on its classpath — no restart dance.

| | |
|---|---|
| JDBC | `jdbc:hive2://localhost:10000` (no auth) |
| Web UI | http://localhost:10002 |

## INSERT/CTAS now works
Previously MR-on-Java-17 broke writes through beeline. With Tez that's resolved — full DDL **and** DML run here.

## Examples
```bash
# DDL + DML + aggregation, all via beeline (Tez DAG)
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000/default -e "
  CREATE DATABASE IF NOT EXISTS demo;
  USE demo;
  DROP TABLE IF EXISTS hello;
  CREATE TABLE hello(id INT, msg STRING) STORED AS ORC;
  INSERT INTO hello VALUES (1,'hive'),(2,'on'),(3,'tez');
  SELECT msg, count(*) c FROM hello GROUP BY msg ORDER BY msg;
"

# confirm engine
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000 -e "SET hive.execution.engine;"

# see tables Spark wrote (shared catalog)
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000/demo -e "SHOW TABLES;"
```

If a write fails with a Java-17 / Kryo error, the Tez framework isn't staged or the `--add-opens` didn't reach the Tez JVMs — see [`tez`](08_tez.md) caveats. Spark-side writes: [`spark-client`](12_spark-client.md).
