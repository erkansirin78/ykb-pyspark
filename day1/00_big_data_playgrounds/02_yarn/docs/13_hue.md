# `hue` — Web UI

`gethue/hue:latest`. One browser front-end over HDFS, YARN, Hive (on Tez) and the metastore Postgres DB. Uses Postgres for its own Django state — see [`postgres`](01_postgres.md).

## Compose service
```yaml
hue:
  image: gethue/hue:latest
  depends_on: [ postgres, hiveserver2, resourcemanager ]
  restart: unless-stopped
  volumes:
    - ./conf/hue/hue.ini:/usr/share/hue/desktop/conf/z-hue.ini:ro
  ports: [ "8888:8888" ]
```
`hue.ini` is mounted as `z-hue.ini` so it loads last and overrides image defaults.

| | |
|---|---|
| URL | http://localhost:8888 |
| Login | `admin` / `admin` (created once, below) |

Connectors: HDFS → `webhdfs://namenode:9870` · YARN → `resourcemanager:8088` (logs proxied via `mr-historyserver:19888`) · Hive → `hiveserver2:10000` · Spark History link → `spark-history:18080` · Postgres editor → `postgres:5432/metastore`.

## One-time: create the admin user
Hue uses `AllowFirstUserDjangoBackend`:
```bash
docker exec hue bash -c "echo \"from django.contrib.auth import get_user_model; U=get_user_model(); u,c=U.objects.get_or_create(username='admin', defaults={'is_superuser':True,'is_staff':True}); u.set_password('admin'); u.is_superuser=True; u.is_staff=True; u.save()\" | /usr/share/hue/build/env/bin/hue shell"
```
**Locked out** (django-axes after 3+ failed tries):
```bash
docker exec hue bash -c "echo 'from axes.models import AccessAttempt; AccessAttempt.objects.all().delete()' | /usr/share/hue/build/env/bin/hue shell"
```

## Examples (in the UI)
1. **Files** — browse `/user/root`, upload, preview a CSV. Mirrors [`namenode`](02_namenode.md).
2. **Editor → Hive** — DDL **and** DML now both work (Hive on Tez):
   ```sql
   CREATE TABLE demo.h(id INT, msg STRING) STORED AS ORC;
   INSERT INTO demo.h VALUES (1,'hue'),(2,'tez');
   SELECT msg, count(*) FROM demo.h GROUP BY msg;
   ```
3. **Editor → Postgres** — inspect the metastore: `SELECT "TBL_NAME" FROM "TBLS";`
4. **Jobs** — running/finished YARN apps (Spark + Tez DAGs), drill into logs, link out to Spark History ([`spark-history`](11_spark-history.md)).

## Health
```bash
docker logs --tail 20 hue
curl -sI http://localhost:8888/ | head -1
```
