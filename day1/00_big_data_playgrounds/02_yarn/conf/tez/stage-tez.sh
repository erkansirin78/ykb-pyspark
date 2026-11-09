#!/usr/bin/env bash
# One-shot: download the Apache Tez binary distribution, extract the client
# libs to a shared volume (consumed by the Hive containers via
# HIVE_AUX_JARS_PATH) and stage tez.tar.gz on HDFS for tez.lib.uris.
# Idempotent: a version marker short-circuits re-runs.
set -euo pipefail

TEZ_VERSION="${TEZ_VERSION:-0.10.4}"
TEZ_HOME="${TEZ_HOME:-/opt/tez}"
HDFS_TEZ_DIR="${HDFS_TEZ_DIR:-/apps/tez}"
MARKER="${TEZ_HOME}/.staged-${TEZ_VERSION}"
TARBALL="apache-tez-${TEZ_VERSION}-bin.tar.gz"
URL="https://archive.apache.org/dist/tez/${TEZ_VERSION}/${TARBALL}"

log() { echo "[tez] $*"; }

# HiveServer2 needs the Tez *client* jars on its classpath. The image's
# /opt/hive/bin/hive only globs `*.jar` out of HIVE_AUX_JARS_PATH when that
# var is a SINGLE directory; a colon-list or a dir containing subdirs is
# passed through verbatim and then localized into the per-query Tez session
# scratch dir, where the `lib/` subdir lands as a directory and Hive tries
# to register it as a FILE resource -> "Path is not a file: .../lib" ->
# "Could not find jar ... Previous writer may have failed to write".
# So assemble ONE flat dir of jar symlinks (no subdirs) for the HS2
# classpath. Pinned to the 0.10.4 jars to match the tez-api bundled in the
# apache/hive:4.0.1 image (avoids two tez-api versions on the classpath).
# Idempotent: rebuilt from scratch on every container start.
CLIENT_DIR="${CLIENT_DIR:-${TEZ_HOME}/client}"
CLIENT_TEZ_VER="${CLIENT_TEZ_VER:-0.10.4}"

build_client_dir() {
  log "assembling flat HS2 client jar dir at ${CLIENT_DIR} (tez ${CLIENT_TEZ_VER})"
  rm -rf "$CLIENT_DIR"
  mkdir -p "$CLIENT_DIR"
  local j
  for j in "${TEZ_HOME}"/tez-*-"${CLIENT_TEZ_VER}".jar \
           "${TEZ_HOME}"/hadoop-shim-"${CLIENT_TEZ_VER}".jar \
           "${TEZ_HOME}"/lib/*.jar; do
    [ -f "$j" ] && ln -sf "$j" "${CLIENT_DIR}/$(basename "$j")"
  done
  # This Tez distro's lib/ ships TWO protobuf-java jars. Tez's DAGProtos is
  # compiled against the one packaged inside tez.tar.gz (the framework the
  # AM runs); shipping the other via HIVE_AUX_JARS_PATH makes Hive localize
  # it onto the Tez AM, where it overrides the framework copy and the AM
  # dies with "GeneratedMessageV3.getUnknownFields ... This is supposed to
  # be overridden by subclasses". Keep only the framework's protobuf.
  local fw_pb
  fw_pb="$(tar -tzf "${TEZ_HOME}/share/tez.tar.gz" 2>/dev/null \
           | sed -n 's#.*/\(protobuf-java-[0-9.]*\.jar\)$#\1#p' | head -1)"
  if [ -n "$fw_pb" ]; then
    log "framework protobuf is ${fw_pb}; dropping any mismatched protobuf-java from client dir"
    local p
    for p in "${CLIENT_DIR}"/protobuf-java-*.jar; do
      [ -e "$p" ] && [ "$(basename "$p")" != "$fw_pb" ] && rm -f "$p"
    done
  fi
  log "client dir has $(ls -1 "$CLIENT_DIR" | wc -l) jars"
}

log "waiting for namenode:9000 ..."
until (echo > /dev/tcp/namenode/9000) >/dev/null 2>&1; do sleep 3; done
log "namenode reachable; waiting for it to leave safe mode ..."
# RPC up != writable: the namenode starts in safe mode (read-only). Poll
# with a heartbeat + timeout instead of the silent `safemode wait`, so a
# slow/stuck namenode is visible rather than looking like a frozen script.
SAFEMODE_TIMEOUT="${SAFEMODE_TIMEOUT:-300}"
elapsed=0
until hdfs dfsadmin -safemode get 2>/dev/null | grep -q 'Safe mode is OFF'; do
  if [ "$elapsed" -ge "$SAFEMODE_TIMEOUT" ]; then
    log "ERROR: still in safe mode after ${SAFEMODE_TIMEOUT}s." >&2
    log "       check: docker exec namenode hdfs dfsadmin -safemode get" >&2
    log "       force: docker exec namenode hdfs dfsadmin -safemode leave" >&2
    exit 1
  fi
  log "  ... still in safe mode (${elapsed}s elapsed)"
  sleep 10
  elapsed=$((elapsed + 10))
done
log "namenode out of safe mode"

if [ -f "$MARKER" ]; then
  log "Tez ${TEZ_VERSION} already staged; refreshing client dir only"
  build_client_dir
  exit 0
fi

mkdir -p "$TEZ_HOME"
# Cache the tarball on the volume so a rerun (e.g. after a safe-mode
# failure) doesn't re-download it.
cd "$TEZ_HOME"

fetch() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$1" "$2"
  elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$1" "$2"
  else
    log "ERROR: neither curl nor wget available in this image" >&2
    exit 1
  fi
}

if [ ! -f "$TARBALL" ]; then
  log "downloading ${URL}"
  fetch "$TARBALL" "$URL"
fi

log "extracting to ${TEZ_HOME}"
tar -xzf "$TARBALL" -C "$TEZ_HOME" --strip-components=1

log "staging share/tez.tar.gz -> hdfs://${HDFS_TEZ_DIR}/tez.tar.gz"
hdfs dfs -mkdir -p "$HDFS_TEZ_DIR"
hdfs dfs -put -f "${TEZ_HOME}/share/tez.tar.gz" "${HDFS_TEZ_DIR}/tez.tar.gz"
hdfs dfs -chmod -R 755 "$HDFS_TEZ_DIR"

build_client_dir

touch "$MARKER"
log "Tez ${TEZ_VERSION} staging complete; one-shot container exiting 0"
