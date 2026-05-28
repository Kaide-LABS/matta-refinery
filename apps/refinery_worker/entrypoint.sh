#!/bin/bash
set -e

# Stage E audit fix: DNS-warmup gate. The container's Celery worker
# previously started before Docker/WSL had populated DNS for
# europe-west4-aiplatform.googleapis.com. Pre-bake dispatches 195
# classify_vertical tasks immediately on boot; without this gate, all
# 195 hit ConnectError("[Errno -5] No address associated with
# hostname") before DNS warms, enter exponential backoff, and pre-bake
# drags from a 5-7 minute window into 40+ minutes.
HOST="${VERTEX_LOCATION:-europe-west4}-aiplatform.googleapis.com"
echo "[entrypoint] Waiting for DNS resolution of ${HOST}..."

START=$(date +%s)
TIMEOUT=60

while true; do
  if getent hosts "${HOST}" >/dev/null 2>&1; then
    ELAPSED=$(($(date +%s) - START))
    echo "[entrypoint] DNS resolved for ${HOST} after ${ELAPSED}s"
    break
  fi

  ELAPSED=$(($(date +%s) - START))
  if [ ${ELAPSED} -gt ${TIMEOUT} ]; then
    echo "[entrypoint] WARNING: DNS for ${HOST} not resolving after ${TIMEOUT}s; starting Celery anyway"
    break
  fi

  sleep 1
done

exec celery -A apps.refinery_worker.app worker --loglevel=INFO --concurrency=4 --pool=gevent
