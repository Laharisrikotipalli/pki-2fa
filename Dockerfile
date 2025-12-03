# Stage 1: Builder - install Python packages into /install
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps used by some packages (cryptography etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install to /install for copying into runtime
COPY requirements.txt /build/requirements.txt
RUN python -m pip install --upgrade pip \
 && python -m pip install --no-cache-dir --target /install -r /build/requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# set timezone to UTC
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/install

WORKDIR /app

# Install system deps: cron and timezone data
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Ensure UTC timezone
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy python packages from builder
COPY --from=builder /install /install

# Copy application code
COPY . /app

# Make cronjob script executable and start script
RUN cp /app/cronjob.sh /usr/local/bin/cronjob.sh \
 && chmod +x /usr/local/bin/cronjob.sh \
 && chmod +x /app/start.sh \
 && chmod 0644 /app/crontab.txt

# Create mount points
VOLUME [ "/data", "/cron" ]

# Expose app port
EXPOSE 8080

# Start cron and http server (start.sh will handle crontab install)
CMD ["/bin/bash", "/app/start.sh"]
