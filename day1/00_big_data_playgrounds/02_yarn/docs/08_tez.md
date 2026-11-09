# `tez` — Apache Tez (Hive execution engine)

**Apache Tez 0.10.3.** Tez is *not* a daemon — it's a YARN execution framework that Hive runs DAGs on instead of MapReduce. There is nothing to keep running; the `tez` service is a **one-shot bootstrap** that exits 0 once Tez is staged.

## Why Tez is here
Hive 4.0.1's MapReduce engine is broken on Java 17 (Kryo plan-serialization: *"Unable to make field … accessible"*). That's why this stack previously said *"don't INSERT/CTAS through HiveServer2"*. **Tez 0.10.3 + the `--add-opens` JVM flags in `tez-site.xml` is the proper fix** — `INSERT` / `CTAS` / joins now run through HiveServer2.

## Compose service (one-shot)
```yaml
tez:
  image: apache/hadoop:3.5.0
  depends_on: [ namenode ]
  environment:
    TEZ_VERSION: "0.10.3"
  entrypoint: ["bash", "/opt/tez-conf/stage-tez.sh"]
  restart: "no"
  volumes:
    - ./conf/tez:/opt/tez-conf:ro
    - tez-dist:/opt/tez
```

`stage-tez.sh` (idempotent — version marker short-circuits re-runs):
1. waits for `namenode:9000`
2. downloads `apache-tez-0.10.3-bin.tar.gz` from `archive.apache.org`
3. extracts client libs to the `tez-dist` volume
4. uploads `share/tez.tar.gz` → `hdfs:///apps/tez/tez.tar.gz` (this is `tez.lib.uris`)
5. exits 0

[`hiveserver2`](10_hiveserver2.md) consumes it: `tez-dist` is mounted read-only at `/opt/tez`, put on the classpath via `HIVE_AUX_JARS_PATH`, and `conf/tez/tez-site.xml` is mounted into Hive's conf dir. `hive-site.xml` sets `hive.execution.engine=tez`.

## Key config (`conf/tez/tez-site.xml`)
| Property | Value | Why |
|---|---|---|
| `tez.lib.uris` | `hdfs:///apps/tez/tez.tar.gz` | framework tarball on HDFS |
| `tez.use.cluster.hadoop-libs` | `true` | use cluster Hadoop jars, avoid version clash |
| `tez.am.launch.cmd-opts` / `tez.task.launch.cmd-opts` | `--add-opens …` | **required** for Java 17, mirrors `mapred-site.xml` |
| `tez.am/task.resource.memory.mb` | `1024` | fits the single 4 GB NodeManager |

## Bring-up order
```bash
docker compose up -d
docker logs -f tez            # watch staging; container should exit "complete"
docker compose ps tez         # State = Exited (0)
docker exec namenode hdfs dfs -ls /apps/tez   # tez.tar.gz present
```
HiveServer2 declares `depends_on: tez: { condition: service_completed_successfully }`, so it does **not** start until this one-shot exits 0 — its classpath always sees the staged Tez jars. No "first query fails / restart hiveserver2" race.

## Examples — INSERT/CTAS via HiveServer2 (now works)
```bash
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000/default -e "
  CREATE DATABASE IF NOT EXISTS tez_demo;
  USE tez_demo;
  CREATE TABLE t(id INT, msg STRING) STORED AS ORC;
  INSERT INTO t VALUES (1,'hive'),(2,'on'),(3,'tez');
  SELECT msg, count(*) FROM t GROUP BY msg ORDER BY msg;
"
```
A successful run logs `Executing on YARN cluster with App id application_… ` and a Tez DAG; find it under http://localhost:8088 (application type **TEZ**).

```bash
# confirm the engine in effect
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000 -e "SET hive.execution.engine;"
# → hive.execution.engine=tez
```

## ⚠️ Status / caveats
- Version-matched to Hive 4.0.1 (built against Tez 0.10.x) and Hadoop 3.5.0, but **this wiring has not been run here** — verify with the bring-up steps above. If the DAG fails on Java 17, the first thing to check is that the `--add-opens` in `tez-site.xml` actually reached the AM/task JVMs (`yarn logs -applicationId …`).
- Needs outbound internet on first `up` to fetch the Tez tarball; afterwards it's cached in the `tez-dist` volume.
- The `apache/hadoop:3.5.0` image must have `curl` or `wget` — the script tries both and errors clearly if neither exists.
- `docker compose down -v` removes `tez-dist`; the next `up` re-downloads and re-stages.
