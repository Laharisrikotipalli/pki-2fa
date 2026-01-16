import os
from datetime import datetime
import pyotp
import base64

def run_cron():
    seed_path = "/data/seed.txt"
    log_path = "/data/cron.log"
    
    if not os.path.exists(seed_path):
        print("Seed file not found.")
        return

    # Read the 64-character seed you just verified
    with open(seed_path, "r") as f:
        hex_seed = f.read().strip()[:64]

    # Generate the TOTP code
    seed_bytes = bytes.fromhex(hex_seed)
    secret = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(secret)
    current_code = totp.now()

    # Required Format for Step 11: YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - 2FA Code: {current_code}\n"

    # Append to the log file
    with open(log_path, "a") as log_file:
        log_file.write(log_entry)
    
    print(f"Logged: {log_entry.strip()}")

if __name__ == "__main__":
    run_cron()