# `mr-historyserver` — MapReduce JobHistory & log server

`apache/hadoop:3.5.0` (Java 17). Serves completed-job history and is the **log server** YARN redirects to (`yarn.log.server.url`), so Hue and the RM UI can show aggregated container logs for finished apps. Web UI on `19888`, history RPC on `10020`.

## Compose service
```yaml
mr-historyserver:
  image: apache/hadoop:3.5.0
  depends_on: [ namenode, resourcemanager ]
  environment:
    WAITFOR: "resourcemanager:8088"
  command: ["mapred", "historyserver"]
```

Even though Hive now runs on Tez (not MR), this server stays useful: it's the log proxy for **all** finished YARN apps (Spark, Tez, MR), since `yarn.nodemanager.remote-app-log-dir=/tmp/yarn-logs` + log-aggregation are enabled.

| | |
|---|---|
| JobHistory UI | http://localhost:19888 |
| History RPC | `mr-historyserver:10020` |

## Examples
```bash
# run an MR job, then find it here
docker exec resourcemanager bash -c \
  "yarn jar \$(ls /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar) pi 2 4"
# → open http://localhost:19888 and look under "Retired Jobs"

# aggregated logs for any finished app (served via this host)
docker exec resourcemanager yarn logs -applicationId <applicationId> | tail -40

# is the history RPC up?
docker exec mr-historyserver bash -c "ss -tlnp 2>/dev/null | grep -E '10020|19888' || netstat -tlnp | grep -E '10020|19888'"
```

From Hue's *Jobs* page, clicking a finished application's logs proxies through here.
