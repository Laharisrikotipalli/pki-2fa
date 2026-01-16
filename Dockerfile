FROM python:3.10-slim

# Install system dependencies for cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# 1. Load the cronjob file into the system crontab
RUN crontab cronjob

# 2. Fix potential Windows line endings and make the script executable
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

# Open the port for FastAPI
EXPOSE 8080

# Execute the startup script
CMD ["./start.sh"]