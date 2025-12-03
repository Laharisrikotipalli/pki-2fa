#!/bin/bash
# start.sh - start cron (daemon) then start uvicorn
set -euo pipefail

# Ensure /data exists
mkdir -p /data

# Start cron daemon
echo "[start.sh] starting cron..."
cron

# Start uvicorn (FastAPI) -- host 0.0.0.0 port 8080
echo "[start.sh] starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
