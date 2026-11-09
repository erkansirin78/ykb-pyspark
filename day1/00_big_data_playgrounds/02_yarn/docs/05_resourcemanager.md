# `resourcemanager` — YARN scheduler

`apache/hadoop:3.5.0` (Java 17). The cluster scheduler: accepts applications, allocates containers across [`nodemanager`](06_nodemanager.md). Spark-on-YARN and MapReduce both submit here. Web UI on `8088`, scheduler RPC on `8032`.

## Compose service
```yaml
resourcemanager:
  image: apache/hadoop:3.5.0
  depends_on: [ namenode ]
  environment:
    WAITFOR: "namenode:9000"
  command: ["yarn", "resourcemanager"]
```

Sizing comes from `conf/hadoop/yarn-site.xml`: 4096 MB / 4 vcores per node, min alloc 256 MB, vmem/pmem checks off (so containers don't get killed on small Docker hosts).

| | |
|---|---|
| ResourceManager UI | http://localhost:8088 |
| Scheduler RPC | `resourcemanager:8032` |

## Examples
```bash
# scheduler + cluster capacity
docker exec resourcemanager yarn node -list -all

# all applications, any state
docker exec resourcemanager yarn application -list -appStates ALL

# drill into one app
docker exec resourcemanager yarn application -status <applicationId>

# classic MapReduce Pi (proves the scheduler works)
docker exec resourcemanager bash -c \
  "yarn jar \$(ls /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar) pi 2 4"
```

Tez DAGs (Hive on Tez) and Spark jobs appear in the same UI at http://localhost:8088. See [`tez`](08_tez.md) and [`spark-client`](12_spark-client.md).
