FROM python:3.10-slim

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set up crontab and startup script
RUN crontab cronjob
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

EXPOSE 8080

CMD ["./start.sh"]