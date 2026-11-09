# Per-service docs

The stack [README](../README.md) covers bring-up and the end-to-end flow. These files break it down **one per docker-compose service** — what it does, its compose snippet, config notes, and runnable examples. Numbered in compose / dependency order.

| # | Service | Role |
|---|---|---|
| [01](01_postgres.md) | `postgres` | Hive metastore + Hue backend |
| [02](02_namenode.md) | `namenode` | HDFS metadata & namespace |
| [03](03_datanode.md) | `datanode` | HDFS block storage |
| [04](04_hdfs-init.md) | `hdfs-init` | HDFS directory bootstrap (one-shot) |
| [05](05_resourcemanager.md) | `resourcemanager` | YARN scheduler |
| [06](06_nodemanager.md) | `nodemanager` | YARN worker |
| [07](07_mr-historyserver.md) | `mr-historyserver` | MR JobHistory + log server |
| [08](08_tez.md) | `tez` | Apache Tez — Hive execution engine (one-shot staging) |
| [09](09_hive-metastore.md) | `hive-metastore` | Shared catalog (Thrift) |
| [10](10_hiveserver2.md) | `hiveserver2` | JDBC SQL endpoint (on Tez) |
| [11](11_spark-history.md) | `spark-history` | Spark History Server |
| [12](12_spark-client.md) | `spark-client` | Spark-on-YARN submission box |
| [13](13_hue.md) | `hue` | Web UI |

Examples assume the stack is up (`docker compose up -d`). HDFS bootstrap is automated by [`hdfs-init`](04_hdfs-init.md) — no manual steps. **Hive runs on [Tez](08_tez.md)** (not MapReduce), so `INSERT`/`CTAS` through HiveServer2/Hue work. (The one remaining manual step in the whole stack is creating the Hue admin user — see the main README §1.)

## Make the web UI cross-links work (host `/etc/hosts`)

The YARN ResourceManager (and HDFS NameNode) build links — e.g. the **ApplicationMaster** / Tez DAG tracking URL — using the *container* hostnames (`http://resourcemanager:8088/proxy/application_…`). Your host browser can't resolve those, so the links 404 unless you hand-edit `resourcemanager` → `localhost` every time.

Fix it once by mapping the container hostnames to loopback in your host's `/etc/hosts`:

```bash
echo '127.0.0.1  resourcemanager nodemanager namenode datanode hiveserver2 hive-metastore spark-history mr-historyserver hue' | sudo tee -a /etc/hosts
```

After this, clicking **ApplicationMaster** in the RM UI (and all NameNode/datanode links) works as-is — no URL editing. The ports are already published to the host by `docker-compose.yaml`, so loopback resolves correctly.

> Caveat: a Tez AM tracking URL only exists **while the query is running** — the AM exits when the DAG finishes (Hive queries are short). For a finished job use `docker exec resourcemanager yarn logs -applicationId <appId>`. Persistent post-mortem Tez history would require the optional Tez UI (YARN Timeline Server + `tez-ui.war`), which this stack deliberately does not deploy — see [08_tez.md](08_tez.md).
