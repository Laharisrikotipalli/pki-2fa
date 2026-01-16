FROM python:3.11-slim

# Install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Setup the Cron Job
RUN echo "* * * * * root /usr/local/bin/python /app/cron_write_totp.py >> /data/cron.log 2>&1" > /etc/cron.d/totp-cron
RUN chmod 0644 /etc/cron.d/totp-cron
RUN touch /etc/default/locale # Required for some cron versions

# Start both cron and the FastAPI app
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8080"]