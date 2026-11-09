# `datanode` — HDFS block storage

`apache/hadoop:3.5.0` (Java 17). Stores and serves the actual file blocks, reporting to [`namenode`](02_namenode.md). Web UI on `9864`. Single-node here (replication 1).

## Compose service
```yaml
datanode:
  image: apache/hadoop:3.5.0
  depends_on: [ namenode ]
  environment:
    WAITFOR: "namenode:9000"
  command: ["hdfs", "datanode"]
  volumes: [ dn-data:/data ]
```

`WAITFOR` blocks startup until the namenode RPC port is up. Blocks persist in the `dn-data` volume until `docker compose down -v`.

| | |
|---|---|
| DataNode UI | http://localhost:9864 |

## Examples
```bash
# is the datanode registered and live?
docker exec namenode hdfs dfsadmin -report | grep -A6 'Live datanodes'

# block report for a file (which datanode holds it)
docker exec namenode hdfs fsck /user/root/people.csv -files -blocks -locations

# datanode-side disk usage
docker exec datanode du -sh /data
```

There is no standalone "datanode CLI"; you operate on it through the namenode (`hdfs dfsadmin`, `hdfs fsck`). UI: http://localhost:9864.
