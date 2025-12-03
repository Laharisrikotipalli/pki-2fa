#!/bin/bash
# /usr/local/bin/cronjob.sh
# Runs generate_totp.py and writes a timestamped TOTP to /data/totp.txt (log)
set -euo pipefail

# Ensure working dir
cd /app || exit 1

# Run the TOTP generator (it will read encrypted_seed.txt and private key)
python3 generate_totp.py >> /data/totp.log 2>&1 || echo "generate_totp failed: $(date)" >> /data/totp.log

