#!/usr/bin/env bash
set -euo pipefail

# ensure python packages in /install are discoverable
export PYTHONPATH=${PYTHONPATH:-/install}

# Run generate_totp.py and append to /data/totp.log
# (do not overwrite; keep historical logs)
# We use python -u for unbuffered output. Protect against missing data dir.
mkdir -p /data
python -u /app/generate_totp.py >> /data/totp.log 2>&1 || true
