# `postgres` — Hive metastore & Hue backend

`postgres:16`. One container, two databases:
- `metastore` (user `hive`) — backing store for the **Hive metastore** schema.
- `hue` (user `hue`) — **Hue's** own Django state; sqlite locks under concurrent Thrift calls and breaks "Error loading databases".

## Compose service
```yaml
postgres:
  image: postgres:16
  environment:
    POSTGRES_USER: hive
    POSTGRES_PASSWORD: hive
    POSTGRES_DB: metastore
  volumes:
    - pg-data:/var/lib/postgresql/data
    - ./init/postgres:/docker-entrypoint-initdb.d:ro
```

The `hue` user + database are auto-created from `init/postgres/01-hue.sql` on first boot; the metastore schema is initialized by [`hive-metastore`](09_hive-metastore.md). No manual steps.

| | |
|---|---|
| Port | `5432` (internal only) |
| Metastore DB | `metastore` / `hive` / `hive` |
| Hue DB | `hue` / `hue` / `hue` |

## Examples
```bash
# interactive shell
docker exec -it postgres psql -U hive -d metastore

# databases registered in the metastore
docker exec postgres psql -U hive -d metastore -c 'SELECT "NAME","DB_LOCATION_URI" FROM "DBS";'

# tables created by Spark/Hive
docker exec postgres psql -U hive -d metastore -c 'SELECT "TBL_NAME","TBL_TYPE" FROM "TBLS";'

# confirm the Hue database exists
docker exec postgres psql -U hive -c '\l' | grep -E 'metastore|hue'
```

State lives in the `pg-data` volume; `docker compose down -v` wipes it and both DBs are recreated on next `up`.
