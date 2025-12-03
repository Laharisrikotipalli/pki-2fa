# Dockerfile
FROM python:3.11-slim

# Prevent Python from writing .pyc and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy project files
COPY . /app

# Install python deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ensure scripts are executable
RUN chmod +x /usr/local/bin/cronjob.sh || true
RUN chmod +x /app/start.sh || true

# Ensure /data exists and owned by root (container will write logs)
RUN mkdir -p /data && chown root:root /data

# Install crontab file into /etc/cron.d and set permissions
COPY crontab.txt /etc/cron.d/pki-cron
RUN chmod 0644 /etc/cron.d/pki-cron
# apply cron job
RUN crontab /etc/cron.d/pki-cron || true

# Expose port
EXPOSE 8080

# Use start.sh to run cron and uvicorn
CMD ["/bin/bash", "/app/start.sh"]
