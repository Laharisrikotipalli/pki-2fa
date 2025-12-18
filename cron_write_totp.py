from pathlib import Path
from totp import generate_totp_code
import os

SEED_FILE = Path("/data/seed.txt")
OUTPUT_FILE = Path("/cron/last_code.txt")

def main():
    if SEED_FILE.exists():
        seed = SEED_FILE.read_text().strip()
        code = generate_totp_code(seed)
        
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(str(code))
        os.chmod(OUTPUT_FILE, 0o666)

if __name__ == "__main__":
    main()