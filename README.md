🚀 PKI-Based Two-Factor Authentication (2FA) Microservice
Built with Python, Flask, RSA-OAEP, TOTP, Cron & Docker

This project implements a fully secure Public Key Infrastructure (PKI) based Two-Factor Authentication (2FA) microservice.
It supports RSA-OAEP encrypted seed decryption, TOTP generation, verification, cron-based logging, and secure storage — all inside Docker.

📌 Features
🔐 1. RSA-OAEP Seed Decryption

Accepts encrypted seed from instructor API

Decrypts using student_private.pem

Saves decrypted seed to /app/keys/seed.txt

⏱ 2. TOTP Generation

Implements RFC 6238

Generates 6-digit codes every 30 seconds

Uses SHA-1 hashing

🧪 3. TOTP Verification

Validates user-provided TOTP

Supports ±1 time-step drift

🕒 4. Cron-Based Code Logging

Runs every minute

Logs TOTP into /app/cron/last_code.txt

📦 5. Fully Containerized

Python 3.11 Slim

Runs on port 8080

Persistent seed using Docker volumes

🗂 Repository Structure
pki-2fa/
│── Dockerfile
│── docker-compose.yml
│── README.md
│── requirements.txt
│── encrypted_seed.txt
│── encrypted_commit_signature.txt
│
├── app/
│   ├── server.py
│   ├── decrypt_seed.py
│   ├── generate_totp.py
│   ├── verify_totp.py
│   └── __init__.py
│
├── keys/
│   ├── instructor_public.pem
│   ├── student_public.pem
│   └── student_private.pem
│
├── cron/
│   └── 2fa-cron
│
└── scripts/
    └── log_2fa_cron.py

🧩 API Endpoints
1. Health Check
GET /health


Response:

{ "service": "pki-2fa", "status": "ok" }

2. Decrypt Seed
POST /decrypt-seed


Body:

{ "encrypted_seed": "<base64>" }


Response:

{ "status": "ok", "message": "Seed decrypted and persisted" }

3. Generate 2FA Code
GET /generate-2fa


Response:

{ "totp": "123456" }

4. Verify 2FA Code
POST /verify-2fa


Body:

{ "totp": "123456" }


Valid:

{ "valid": true }


Invalid:

{ "valid": false }

🧱 Docker Setup
Build & Run
docker compose up -d --build

Check logs
docker compose logs --tail=100

Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/generate-2fa

🕒 Cron Job

Cron file:

* * * * * root cd /app && /usr/local/bin/python3 scripts/log_2fa_cron.py >> /app/cron/last_code.txt 2>&1


Check output:

docker exec -it <container> tail -n 20 /app/cron/last_code.txt

🔑 Key Files
File	Purpose
student_private.pem	Required for decryption & commit signature
student_public.pem	Submitted to instructor
instructor_public.pem	Encrypts commit signature

⚠️ These keys are ONLY for course use. Do NOT reuse elsewhere.

📝 Submission Artifacts

encrypted_seed.txt

encrypted_commit_signature.txt

student_public.pem

student_private.pem (required)

All source files

Docker + Cron setup

✔️ Verify Before Submission
curl http://localhost:8080/health
curl http://localhost:8080/generate-2fa
curl -X POST http://localhost:8080/verify-2fa -d '{"totp":"123456"}' -H "Content-Type: application/json"
docker exec -it $(docker ps -q) tail -n 20 /app/cron/last_code.txt
docker compose restart

🧑‍💻 Author

Lahari Sri
B.Tech CSE — PKI-2FA Microservice Implementation
