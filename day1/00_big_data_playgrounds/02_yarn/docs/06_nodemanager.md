# `nodemanager` — YARN worker

`apache/hadoop:3.5.0` (Java 17). The worker that launches and monitors containers (Spark executors, Tez/MR tasks, app masters) on behalf of the [`resourcemanager`](05_resourcemanager.md). Web UI on `8042`. Runs the `mapreduce_shuffle` aux-service.

## Compose service
```yaml
nodemanager:
  image: apache/hadoop:3.5.0
  depends_on: [ resourcemanager ]
  environment:
    WAITFOR: "resourcemanager:8088"
  command: ["yarn", "nodemanager"]
```

Resource envelope (from `yarn-site.xml`): `yarn.nodemanager.resource.memory-mb=4096`, `cpu-vcores=4`. All containers in the stack fit inside this one NM — keep app/driver/AM memory modest.

| | |
|---|---|
| NodeManager UI | http://localhost:8042 |

## Examples
```bash
# node health + available resources as seen by the RM
docker exec resourcemanager yarn node -list -showDetails

# containers currently running on this node
docker exec nodemanager jps

# aggregated container logs for a finished app (log-aggregation is on)
docker exec resourcemanager yarn logs -applicationId <applicationId> | head -50
```

If a Spark/Tez job hangs in `ACCEPTED`, it's almost always this node out of memory — lower `spark.executor.memory` / `hive.tez.container.size`. Logs are proxied through [`mr-historyserver`](07_mr-historyserver.md).
