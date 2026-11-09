# `hdfs-init` — HDFS bootstrap (one-shot)

`apache/hadoop:3.5.0`. **Not a daemon** — a one-shot that creates the HDFS directory layout the rest of the stack needs, then exits 0. Replaces the manual bootstrap that used to be a README step, so `docker compose down -v && up -d` works hands-free.

## Compose service (one-shot)
```yaml
hdfs-init:
  image: apache/hadoop:3.5.0
  depends_on: [ namenode, datanode ]
  entrypoint: ["bash", "/opt/init/bootstrap-hdfs.sh"]
  restart: "no"
  volumes:
    - ./conf/hadoop/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml:ro
    - ./conf/hadoop/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml:ro
    - ./conf/init:/opt/init:ro
```

`bootstrap-hdfs.sh` (idempotent):
1. waits for `namenode:9000`, then polls until **safe mode is OFF** (heartbeat every 10s, 300s timeout — never a silent hang)
2. `mkdir -p /spark-logs /tmp /user/hive/warehouse /user/hue /user/spark /tmp/yarn-logs`
3. `chmod -R 1777 /tmp /user/hive/warehouse /spark-logs`
4. `chown hue:hue /user/hue` · `chown spark:spark /user/spark`
5. exits 0

## Why it gates other services
`hive-metastore`, `spark-history`, `hue` (and indirectly `hiveserver2` via the chain) declare:
```yaml
depends_on:
  hdfs-init:
    condition: service_completed_successfully
```
So they only start once the directories exist. Without this, `spark-history` hard-fails (`/spark-logs` missing) and loops on `restart: unless-stopped`.

## Safe mode, explained
Every NameNode start begins in safe mode (read-only) until block-report quorum + a 30s extension. This dev stack sets `dfs.namenode.safemode.threshold-pct=0` and `safemode.extension=0` in `hdfs-site.xml`, so it leaves safe mode at startup — `hdfs-init` proceeds within seconds instead of stalling 30–90s on every `up`.

## Examples
```bash
# watch it run
docker compose logs -f hdfs-init     # ends "HDFS bootstrap complete; ... exiting 0"
docker compose ps -a hdfs-init       # State = Exited (0)

# verify the layout
docker exec namenode hdfs dfs -ls /
docker exec namenode hdfs dfs -ls /user
docker exec namenode hdfs dfs -stat '%a %u:%g' /user/hue   # 755 hue:hue

# re-run by hand if ever needed (idempotent)
docker compose up -d --force-recreate hdfs-init
```

If it exits non-zero with "still in safe mode after 300s", the NameNode genuinely didn't recover — check `docker exec namenode hdfs dfsadmin -safemode get` and the [`datanode`](03_datanode.md)/[`namenode`](02_namenode.md) logs.
