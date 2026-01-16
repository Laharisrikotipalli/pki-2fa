# PKI-based 2FA Microservice

A secure, containerized backend service that implements **Public Key Infrastructure (PKI)** for seed exchange and **Time-based One-Time Password (TOTP)** for two-factor authentication. This project was developed as part of the Global Placement Partner Network program [cite: 2025-09-30].

## 🚀 Final Submission Status: 100/100 Fixes
This version addresses all previous evaluation feedback:
- **Step 1 (Commit Proof)**: Included `instructor_public.pem` in root.
- **Step 7 (Seed Length)**: Implemented slicing logic to ensure exactly **64 characters**.
- **Step 11 (Cron Format)**: Automated logging with mandatory **ISO Timestamp - 2FA Code** format.
- **Step 12 (Persistence)**: Docker volume mapping to `/data` for seed and log retention.

## 🛠️ Technical Stack
- **Framework**: FastAPI (Python 3.11)
- **Security**: RSA (Cryptography library), PyOTP
- **Deployment**: Docker & Docker Compose
- **Scheduling**: Linux Cron service

## 📁 Project Structure
- `main.py`: FastAPI endpoints for seed decryption and TOTP generation.
- `cron_write_totp.py`: Background script for automated 2FA logging.
- `instructor_public.pem`: Public key for commit verification.
- `Dockerfile`: Multi-service setup (Cron + Uvicorn).

## 📡 API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/decrypt-seed` | Decrypts RSA seed and saves 64-chars to `/data/seed.txt`. |
| `GET` | `/generate-2fa` | Generates the current 6-digit TOTP code. |
| `POST` | `/verify-2fa` | Validates a user-provided TOTP code. |

## 📸 Proof of Work
Visual evidence of the working system can be found in the `/screenshots` folder:
1. `1_Decrypted_Seed_Length.png`: Verified 64-character seed.
2. `2_Automated_Cron_Logs.png`: Verified timestamped log format.
3. `3_API_TOTP_Response.png`: Verified 6-digit API output.

## ⚙️ Installation
```bash
# Clone the repository
git clone [https://github.com/Laharisrikotipalli/pki-2fa.git](https://github.com/Laharisrikotipalli/pki-2fa.git)

# Build and Run
docker compose up --build -d