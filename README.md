PKI-Based 2FA System (TOTP) 

This repository contains the full implementation of a Public Key Infrastructure (PKI) based Two-Factor Authentication (2FA) system using RSA-OAEP decryption and Time-based One-Time Passwords (TOTP).

This project implements:

RSA key generation

Encrypted seed decryption

TOTP generation

REST API endpoints

Docker deployment

Cron job for automated OTP logging

## 1. Student Details
Field	Value
Student ID	YOUR_STUDENT_ID
GitHub Repo URL (must match instructor request)	https://github.com/Laharisrikotipalli/pki-2fa
## 2. Project Structure
pki-2fa/
│
├── app/
│   ├── server.py              # Main API server
│   ├── decrypt_seed.py        # RSA-OAEP seed decryption
│   ├── totp_utils.py          # TOTP utilities
│   └── __init__.py
│
├── scripts/
│   └── log_2fa_cron.py        # Cron script to log OTP every minute
│
├── cron/
│   └── 2fa-cron               # Cron configuration (must be LF)
│
├── encrypted_seed.txt         # Encrypted seed received from instructor API
├── student_private.pem        # Student RSA private key
├── student_public.pem         # Student RSA public key
├── instructor_public.pem      # Instructor RSA public key
│
├── Dockerfile                 # Build instructions
├── docker-compose.yml         # Container orchestration
└── README.md                  # Project documentation

## 3. Installation & Setup
3.1 Install Dependencies (Local Development)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

## 4. Running the Server
4.1 Run Locally
python app/server.py


Server runs at:

http://127.0.0.1:8080

4.2 Run Using Docker
docker-compose up --build -d


View logs:

docker-compose logs -f

## 5. API Endpoints
1️⃣ GET /get-public-key

Returns the student’s public RSA key.

Example:

curl http://127.0.0.1:8080/get-public-key

2️⃣ POST /decrypt-seed

Decrypts the encrypted seed using RSA-OAEP + SHA-256.

Request:

{
  "encrypted_seed": "<contents of encrypted_seed.txt>"
}


Example cURL:

curl -X POST http://127.0.0.1:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\":\"$(tr -d '\r\n' < encrypted_seed.txt)\"}"

3️⃣ POST /generate-otp

Generates a TOTP code using the decrypted seed.

Example cURL:

curl -X POST http://127.0.0.1:8080/generate-otp \
  -H "Content-Type: application/json" \
  -d '{"student_id": "YOUR_STUDENT_ID"}'


Response:

{
  "otp": "123456"
}

## 6. Cron Job (Automated OTP Logging)

The cron job logs a new TOTP value every minute.

Cron config: cron/2fa-cron

(MUST use LF line endings)

* * * * * cd /app && /usr/local/bin/python3 scripts/log_2fa_cron.py >> /cron/last_code.txt 2>&1


Check the log inside the container:

docker exec -it <container_id> cat /cron/last_code.txt

## 7. Security Details
RSA Decryption

Algorithm: RSA-OAEP

Hash: SHA-256

MGF1: SHA-256

TOTP Algorithm

Hash: SHA-1

Digits: 6

Time window: 30 seconds

## 8. Submission Checklist
Requirement	Status
student_private.pem & student_public.pem in root	✔️
instructor_public.pem in root	✔️
encrypted_seed.txt added to root	✔️
/get-public-key implemented	✔️
/decrypt-seed implemented	✔️
/generate-otp implemented	✔️
Dockerfile works	✔️
docker-compose works	✔️
Cron job logs OTP	✔️
README complete	✔️
## 9. Final Notes

This repository contains all required components for PKI-based 2FA evaluation.
Ensure your encrypted_seed.txt matches the seed received from the instructor API using THIS EXACT GitHub URL.
