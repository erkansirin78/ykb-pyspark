# Hadoop + Hive + Spark on YARN with Hue

Split-image stack:
- HDFS + YARN — `apache/hadoop:3.5.0` (Java 17)
- Hive metastore + HiveServer2 — `apache/hive:4.0.1` (postgres-backed)
- Apache Tez 0.10.3 — Hive's execution engine (one-shot staging container)
- Spark on YARN + Spark History Server — `spark:4.1.3-java21-python3`
- Hue UI — `gethue/hue:latest`
- Postgres for Hive metastore — `postgres:16`

Single docker network (`vbo`); each role is its own container.

## 1. Bring up the stack
```bash
docker compose up -d
docker compose ps          # daemons Up; hdfs-init & tez = Exited (0)
```

That's it — **no manual HDFS bootstrap**. On `up` (including after a full `down -v`) the stack self-initializes, in order:

1. `namenode` auto-formats; leaves safe mode immediately (`dfs.namenode.safemode.threshold-pct=0`).
2. `hdfs-init` (one-shot) waits for HDFS to be writable, then creates the directory layout (`/spark-logs`, `/user/hive/warehouse`, `/user/hue`, …) with correct perms/owners, and exits 0.
3. `tez` (one-shot) stages `tez.tar.gz` on HDFS, exits 0.
4. `hive-metastore`, `hiveserver2`, `spark-history`, `hue` start only **after** their one-shots complete (`depends_on: condition: service_completed_successfully`), so there's no "started too early" race — in particular HiveServer2 always comes up with the Tez jars on its classpath.

Everything is idempotent; re-`up` after a plain `down` reuses staged state.

> Hue uses Postgres for its own state (sqlite locks under concurrent Thrift calls and breaks "Error loading databases" in the UI). The `hue` user + database are auto-created from `init/postgres/01-hue.sql` on first boot of the postgres container; no manual step needed.

**One manual step remains — create the Hue admin user** (Hue uses `AllowFirstUserDjangoBackend`):
```bash
docker exec hue bash -c "echo \"from django.contrib.auth import get_user_model; U=get_user_model(); u,c=U.objects.get_or_create(username='admin', defaults={'is_superuser':True,'is_staff':True}); u.set_password('admin'); u.is_superuser=True; u.is_staff=True; u.save()\" | /usr/share/hue/build/env/bin/hue shell"
```
Then log in at http://localhost:8888/ as `admin`/`admin`.

> **If login is rejected as "Invalid username or password" after 3+ tries:** django-axes locked your IP. Clear it:
> ```bash
> docker exec hue bash -c "echo 'from axes.models import AccessAttempt; AccessAttempt.objects.all().delete()' | /usr/share/hue/build/env/bin/hue shell"
> ```

## 2. Web UIs
| Service             | URL                       |
|---------------------|---------------------------|
| HDFS NameNode       | http://localhost:9870     |
| YARN ResourceManager| http://localhost:8088     |
| YARN NodeManager    | http://localhost:8042     |
| MR JobHistory       | http://localhost:19888    |
| Spark History       | http://localhost:18080    |
| HiveServer2 WebUI   | http://localhost:10002    |
| Hue                 | http://localhost:8888     |

HiveServer2 JDBC: `jdbc:hive2://localhost:10000` (no auth). Hive metastore Thrift: `localhost:9083`.

## 3. Smoke tests

**HDFS:**
```bash
docker exec namenode hdfs dfsadmin -report | head -20
```

**YARN MR (Pi):**
```bash
docker exec resourcemanager bash -c "yarn jar \$(ls /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar) pi 2 4"
```

**Spark on YARN (Pi):**
```bash
docker exec spark-client /opt/spark/bin/spark-submit \
  --master yarn --deploy-mode client \
  --conf spark.driver.host=spark-client \
  --class org.apache.spark.examples.SparkPi \
  /opt/spark/examples/jars/spark-examples_2.13-4.1.3.jar 5
```

**Spark SQL writing to Hive metastore on YARN:**
```bash
docker exec spark-client /opt/spark/bin/spark-sql \
  --master yarn --conf spark.driver.host=spark-client -e "
    CREATE DATABASE IF NOT EXISTS demo;
    USE demo;
    DROP TABLE IF EXISTS hello_spark;
    CREATE TABLE hello_spark(id INT, msg STRING) USING PARQUET;
    INSERT INTO hello_spark VALUES(1,'spark'),(2,'on'),(3,'yarn');
    SELECT * FROM hello_spark ORDER BY id;
  "
```

The first invocation downloads Hive 4.0.1 client jars via Maven (~300MB cached at `/tmp/.ivy2`); subsequent runs are fast.

**HiveServer2 INSERT/CTAS on Tez (beeline):**
```bash
docker exec hiveserver2 beeline -u jdbc:hive2://localhost:10000/default -e "
  CREATE DATABASE IF NOT EXISTS demo;
  USE demo;
  CREATE TABLE IF NOT EXISTS hello_hive(id INT, msg STRING) STORED AS ORC;
  INSERT INTO hello_hive VALUES (1,'hive'),(2,'on'),(3,'tez');
  SELECT msg, count(*) FROM hello_hive GROUP BY msg ORDER BY msg;
"
```
Runs as a Tez DAG (application type **TEZ** in the YARN UI). Requires the `tez` one-shot to have staged `tez.tar.gz` on HDFS first — see §4.

## 4. Hive runs on Apache Tez (not MapReduce)
Hive 4.0.1's MapReduce engine is incompatible with Java 17 (Kryo plan-serialization breaks — *"Unable to make field … accessible"* / *"unregistered class ID"*). **This stack switches Hive to Apache Tez 0.10.3**, which — with the `--add-opens` flags in `conf/tez/tez-site.xml` — runs `INSERT`/`CTAS`/joins through HiveServer2 successfully.

How it's wired:
- `tez` — a **one-shot** container that downloads Tez, extracts client jars to the `tez-dist` volume, and stages `tez.tar.gz` on `hdfs:///apps/tez/`, then exits 0.
- `hiveserver2` mounts `tez-dist` (classpath via `HIVE_AUX_JARS_PATH`) + `tez-site.xml`; `hive-site.xml` sets `hive.execution.engine=tez`.

```bash
docker logs -f tez                            # watch staging; ends "staging complete"
docker compose ps tez                         # State = Exited (0)
docker exec namenode hdfs dfs -ls /apps/tez   # tez.tar.gz present
```
HiveServer2 declares `depends_on: tez: { condition: service_completed_successfully }`, so it only starts after Tez staging finishes — no first-query race, no manual restart. Spark on YARN does **not** use Tez (Spark has its own DAG engine); both Spark SQL and Hive write to the same metastore and see each other's tables. Full detail: [docs/08_tez.md](docs/08_tez.md).

## 5. Hue
Login: any username (`AllowAllBackend`). Configured connectors:
- HDFS browser → `webhdfs://namenode:9870`
- YARN apps → `resourcemanager:8088` (proxy to NM/AM logs via `mr-historyserver:19888`)
- Hive editor → `hiveserver2:10000`
- Spark History link → `spark-history:18080`
- Postgres editor (metastore DB) → `postgres:5432/metastore` as `hive/hive`

## 6. Java 17 notes baked into the configs
The configs already include the workarounds for the Java 17 strong-encapsulation issues. Worth knowing about if you change them:
- `mapred-site.xml` ships the canonical `--add-opens` list under `mapreduce.{map,reduce}.java.opts` and `yarn.app.mapreduce.am.command-opts` (covers `java.lang`, `java.io`, `java.net`, `java.nio`, `java.util.concurrent.atomic`, `sun.nio.ch`, etc.).
- `tez-site.xml` repeats that same `--add-opens` list under `tez.am.launch.cmd-opts` / `tez.task.launch.cmd-opts` — without it Hive-on-Tez DAGs fail on Java 17 exactly like MR did.
- `spark-defaults.conf` pins `spark.sql.hive.metastore.version=4.0.1` with `spark.sql.hive.metastore.jars=maven` — Spark 4.1.3 ships Hive 2.3.10 client jars by default and would call `get_table` on a Hive 4 metastore (which renamed it).
- `spark-client` runs with `_JAVA_OPTIONS=-Duser.home=/tmp` because the official Spark image's `spark` user has `HOME=/nonexistent` in `/etc/passwd`, which Ivy reads via `user.home` for its cache.

## 7. Shutdown
```bash
docker compose down            # keep HDFS / metastore data
docker compose down -v         # full reset (fresh format / fresh schema)
```

## 8. Layout
```
02_yarn/
├── docker-compose.yaml
├── conf/
│   ├── hadoop/        # core-site, hdfs-site, yarn-site, mapred-site
│   ├── hive/          # hive-site
│   ├── tez/           # tez-site.xml + stage-tez.sh (one-shot Tez staging)
│   ├── init/          # bootstrap-hdfs.sh (one-shot HDFS dir bootstrap)
│   ├── spark/         # spark-defaults
│   └── hue/           # hue.ini (mounted as z-hue.ini override)
├── init/
│   └── postgres/      # 01-hue.sql (auto-creates the Hue DB on first boot)
├── jars/
│   └── postgresql-42.7.4.jar   # mounted into Hive containers as JDBC driver
├── docs/                       # per-service guides + examples
└── README.md
```

## 9. Per-service docs
This README is the end-to-end view. For a per-service breakdown — one file per docker-compose service (role, compose snippet, config notes, runnable examples) — see [`docs/`](docs/README.md):

| # | Service | Doc |
|---|---|---|
| 01 | `postgres` | [docs/01_postgres.md](docs/01_postgres.md) |
| 02 | `namenode` | [docs/02_namenode.md](docs/02_namenode.md) |
| 03 | `datanode` | [docs/03_datanode.md](docs/03_datanode.md) |
| 04 | `hdfs-init` | [docs/04_hdfs-init.md](docs/04_hdfs-init.md) |
| 05 | `resourcemanager` | [docs/05_resourcemanager.md](docs/05_resourcemanager.md) |
| 06 | `nodemanager` | [docs/06_nodemanager.md](docs/06_nodemanager.md) |
| 07 | `mr-historyserver` | [docs/07_mr-historyserver.md](docs/07_mr-historyserver.md) |
| 08 | `tez` | [docs/08_tez.md](docs/08_tez.md) |
| 09 | `hive-metastore` | [docs/09_hive-metastore.md](docs/09_hive-metastore.md) |
| 10 | `hiveserver2` | [docs/10_hiveserver2.md](docs/10_hiveserver2.md) |
| 11 | `spark-history` | [docs/11_spark-history.md](docs/11_spark-history.md) |
| 12 | `spark-client` | [docs/12_spark-client.md](docs/12_spark-client.md) |
| 13 | `hue` | [docs/13_hue.md](docs/13_hue.md) |
