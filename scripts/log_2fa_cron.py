#!/usr/bin/env python3
"""
Cron script to log 2FA codes every minute.

Reads a hex seed from /data/seed.txt, converts to base32 (for compatibility),
generates a 6-digit TOTP (HMAC-SHA1, 30s window) and prints a line:

YYYY-MM-DD HH:MM:SS 2FA Code: 123456
"""

from __future__ import annotations
import time
import hmac
import hashlib
import struct
from datetime import datetime, timezone
from pathlib import Path
import base64
import sys

SEED_PATH = Path("/data/seed.txt")
DIGITS = 6
STEP = 30  # seconds

def read_hex_seed(path: Path) -> bytes | None:
    try:
        s = path.read_text().strip()
    except FileNotFoundError:
        return None
    if not s:
        return None
    s = "".join(s.split())
    try:
        return bytes.fromhex(s)
    except ValueError:
        return None

def hex_to_base32(hex_bytes: bytes) -> str:
    """Return RFC4648 base32 string without padding (uppercase)."""
    b32 = base64.b32encode(hex_bytes).decode('ascii')
    # remove '=' padding to match many base32 TOTP conventions
    return b32.rstrip('=')

def totp_from_secret_bytes(secret_bytes: bytes, digits: int = DIGITS, step: int = STEP, algo=hashlib.sha1) -> str:
    """Generate TOTP directly from raw secret bytes (HMAC-SHA1)."""
    counter = int(time.time() // step)
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(secret_bytes, counter_bytes, algo).digest()
    offset = hmac_hash[-1] & 0x0F
    code_int = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7fffffff
    return str(code_int % (10**digits)).zfill(digits)

def utc_timestamp_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def main() -> int:
    secret_bytes = read_hex_seed(SEED_PATH)
    if secret_bytes is None:
        print(f"{utc_timestamp_now()} 2FA Code: ERROR - seed missing or invalid", flush=True)
        return 2

    # for compatibility: show base32 if needed (not used for generation below)
    try:
        base32_secret = hex_to_base32(secret_bytes)
    except Exception:
        base32_secret = None

    try:
        code = totp_from_secret_bytes(secret_bytes)
    except Exception as e:
        print(f"{utc_timestamp_now()} 2FA Code: ERROR - {e}", flush=True)
        return 3

    print(f"{utc_timestamp_now()} 2FA Code: {code}", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
