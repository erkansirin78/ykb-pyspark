#!/usr/bin/env bash
# One-shot: create the HDFS directory layout the stack needs (warehouse,
# spark event logs, per-user dirs, yarn log dir) with the right perms/owners.
# Replaces the manual bootstrap that used to be a README step. Idempotent.
set -euo pipefail

log() { echo "[hdfs-init] $*"; }

log "waiting for namenode:9000 ..."
until (echo > /dev/tcp/namenode/9000) >/dev/null 2>&1; do sleep 3; done

log "namenode reachable; waiting for it to leave safe mode ..."
SAFEMODE_TIMEOUT="${SAFEMODE_TIMEOUT:-300}"
elapsed=0
until hdfs dfsadmin -safemode get 2>/dev/null | grep -q 'Safe mode is OFF'; do
  if [ "$elapsed" -ge "$SAFEMODE_TIMEOUT" ]; then
    log "ERROR: still in safe mode after ${SAFEMODE_TIMEOUT}s." >&2
    log "       check: docker exec namenode hdfs dfsadmin -safemode get" >&2
    exit 1
  fi
  log "  ... still in safe mode (${elapsed}s elapsed)"
  sleep 10
  elapsed=$((elapsed + 10))
done
log "namenode out of safe mode"

log "creating directory layout"
hdfs dfs -mkdir -p /spark-logs /tmp /user/hive/warehouse /user/hue /user/spark /tmp/yarn-logs
hdfs dfs -chmod -R 1777 /tmp /user/hive/warehouse /spark-logs
hdfs dfs -chown hue:hue /user/hue
hdfs dfs -chown spark:spark /user/spark

log "done:"
hdfs dfs -ls / 2>/dev/null || true
log "HDFS bootstrap complete; one-shot container exiting 0"
