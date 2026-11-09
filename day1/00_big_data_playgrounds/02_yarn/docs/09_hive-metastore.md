# `hive-metastore` — shared catalog (Thrift)

`apache/hive:4.0.1`, Postgres-backed. The metastore Thrift service on `9083` — the single catalog [`hiveserver2`](10_hiveserver2.md) and [`spark-client`](12_spark-client.md) both read/write. It does no query execution.

## Compose service
```yaml
hive-metastore:
  image: apache/hive:4.0.1
  depends_on: [ postgres, namenode ]
  environment:
    SERVICE_NAME: metastore
    DB_DRIVER: postgres
    VERBOSE: "true"
  volumes:
    - ./conf/hive/hive-site.xml:/opt/hive/conf/hive-site.xml:ro
    - ./jars/postgresql-42.7.4.jar:/opt/hive/lib/postgresql-42.7.4.jar:ro
  ports: [ "9083:9083" ]
```

Schema auto-initializes against Postgres (`metastore` DB) on first boot. JDBC config + warehouse dir (`/user/hive/warehouse`) come from `conf/hive/hive-site.xml`.

| | |
|---|---|
| Metastore Thrift | `localhost:9083` / `hive-metastore:9083` |
| Warehouse | `hdfs:///user/hive/warehouse` |

## Examples
```bash
# Thrift port up?
docker exec hive-metastore bash -c "ss -tlnp 2>/dev/null | grep 9083 || netstat -tlnp | grep 9083"

# schema version (proves init succeeded)
docker exec postgres psql -U hive -d metastore -c 'SELECT * FROM "VERSION";'

# everything Spark/Hive registered
docker exec postgres psql -U hive -d metastore -c 'SELECT "TBL_NAME" FROM "TBLS";'

# metastore-side logs (VERBOSE=true)
docker logs --tail 40 hive-metastore
```

The catalog is shared: a table written by Spark on YARN ([`spark-client`](12_spark-client.md)) is immediately visible to HiveServer2 and Hue, and vice-versa.
