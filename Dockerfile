# Dockerfile (fixed and minimal for PKI-2FA)
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install cron and required system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron openssl && \
    rm -rf /var/lib/apt/lists/*

# Copy entire project into image
COPY . /app

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy cron file into /etc/cron.d (if present) and set permissions
RUN if [ -f /app/cron/2fa-cron ]; then \
      cp /app/cron/2fa-cron /etc/cron.d/2fa-cron && \
      chmod 0644 /etc/cron.d/2fa-cron; \
    fi

# Make start script executable
RUN chmod +x /app/start.sh || true

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["/app/start.sh"]
