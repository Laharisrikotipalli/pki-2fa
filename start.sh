#!/bin/bash

# 1. Prepare directories and log file
mkdir -p /data /cron
touch /var/log/cron.log
chmod 777 /data /cron /var/log/cron.log

# 2. Fix line endings for the cronjob file inside the container
sed -i 's/\r$//' /app/cronjob

# 3. Load the cronjob file into the system
crontab /app/cronjob

# 4. Start the background service
service cron start

# 5. Start the web server
exec uvicorn main:app --host 0.0.0.0 --port 8080