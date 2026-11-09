# `namenode` — HDFS metadata & namespace

`apache/hadoop:3.5.0` (Java 17). Holds the filesystem namespace + block map. Web UI on `9870`, RPC on `9000` (`fs.defaultFS = hdfs://namenode:9000`). Pairs with [`datanode`](03_datanode.md) for block storage.

## Compose service
```yaml
namenode:
  image: apache/hadoop:3.5.0
  environment:
    ENSURE_NAMENODE_DIR: "/data/nn"
  command: ["hdfs", "namenode"]
  volumes: [ nn-data:/data ]
```

Auto-formats `/data/nn` on first boot. Namespace persists in the `nn-data` volume until `docker compose down -v`.

| | |
|---|---|
| NameNode UI | http://localhost:9870 |
| RPC | `hdfs://namenode:9000` |

## Directory bootstrap — automated
The HDFS layout (`/spark-logs`, `/user/hive/warehouse`, `/user/hue`, …) is created automatically on every `up` by the one-shot [`hdfs-init`](04_hdfs-init.md) — no manual step, even after `down -v`. Safe mode is configured to clear at startup (`dfs.namenode.safemode.threshold-pct=0`, `safemode.extension=0` in `hdfs-site.xml`), so it never stalls writes.

## Examples
```bash
# cluster health
docker exec namenode hdfs dfsadmin -report | head -20

# put a local file in and read it back
docker exec namenode bash -c \
  "echo -e 'id,name\n1,alice\n2,bob' > /tmp/people.csv && \
   hdfs dfs -mkdir -p /user/root && \
   hdfs dfs -put -f /tmp/people.csv /user/root/people.csv && \
   hdfs dfs -cat /user/root/people.csv"

# usage + block check
docker exec namenode hdfs dfs -du -h /user
docker exec namenode hdfs fsck /user/root/people.csv -files -blocks
```

Same `hdfs://namenode:9000/user/root/...` path Spark reads in [`spark-client`](12_spark-client.md).
