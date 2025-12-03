# app/main.py  (Flask replacement with robust secret handling)
from flask import Flask, jsonify
from pathlib import Path
import os
import base64
import re
import pyotp
from decrypt_seed import decrypt_seed

app = Flask(__name__)

ENCRYPTED_FILE = os.environ.get("ENCRYPTED_SEED_FILE", "encrypted_seed.txt")
PRIVATE_KEY_FILE = os.environ.get("PRIVATE_KEY_FILE", "student_private.pem")

def load_files():
    enc_path = Path(ENCRYPTED_FILE)
    pk_path = Path(PRIVATE_KEY_FILE)
    if not enc_path.exists():
        raise FileNotFoundError(f"{ENCRYPTED_FILE} not found")
    if not pk_path.exists():
        raise FileNotFoundError(f"{PRIVATE_KEY_FILE} not found")
    return enc_path.read_text().strip(), pk_path.read_bytes()

def is_base64(s: str) -> bool:
    s = s.strip()
    if not s:
        return False
    # base64 characters + possible padding and whitespace
    if re.fullmatch(r'[A-Za-z0-9+/=\s]+', s):
        try:
            data = base64.b64decode(s, validate=True)
            return len(data) >= 4
        except Exception:
            return False
    return False

def is_hex(s: str) -> bool:
    s = s.strip()
    return bool(re.fullmatch(r'[0-9a-fA-F]+', s)) and (len(s) % 2 == 0)

def to_base32_from_base64(s: str) -> str:
    b = base64.b64decode(s)
    return base64.b32encode(b).decode('utf-8').strip('=')

def to_base32_from_hex(s: str) -> str:
    b = bytes.fromhex(s)
    return base64.b32encode(b).decode('utf-8').strip('=')

def to_base32_from_bytes_string(s: str) -> str:
    b = s.encode('utf-8')
    return base64.b32encode(b).decode('utf-8').strip('=')

def try_generate_totp_from_seed(seed_str: str):
    """
    Try several interpretations of the decrypted seed and return a tuple (otp, info)
    where info describes which method succeeded.
    Raises ValueError if none succeed.
    """
    seed_original = (seed_str or "").strip()
    # 1) try as-is
    try:
        otp = pyotp.TOTP(seed_original).now()
        return otp, "raw"
    except Exception:
        pass

    # normalize (remove whitespace, uppercase)
    candidate = re.sub(r'\s+', '', seed_original).upper()
    try:
        otp = pyotp.TOTP(candidate).now()
        return otp, "normalized"
    except Exception:
        pass

    # handle base64 -> base32
    try:
        if is_base64(seed_original):
            b32 = to_base32_from_base64(seed_original)
            otp = pyotp.TOTP(b32).now()
            return otp, "base64->base32"
    except Exception:
        pass

    # handle hex -> base32
    try:
        if is_hex(seed_original):
            b32 = to_base32_from_hex(seed_original)
            otp = pyotp.TOTP(b32).now()
            return otp, "hex->base32"
    except Exception:
        pass

    # fallback: treat as UTF-8 bytes -> base32
    try:
        b32 = to_base32_from_bytes_string(seed_original)
        otp = pyotp.TOTP(b32).now()
        return otp, "bytes->base32"
    except Exception:
        pass

    # all attempts failed
    raise ValueError("secret not in a recognized format")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/totp")
def totp_endpoint():
    # load encrypted seed and private key
    try:
        enc, priv = load_files()
    except Exception as e:
        return jsonify({"error": f"Configuration error: {e}"}), 500

    # decrypt
    try:
        seed = decrypt_seed(enc, priv)
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {e}"}), 500

    # generate TOTP using robust detection
    try:
        otp, info = try_generate_totp_from_seed(seed)
        return jsonify({"otp": otp, "method": info})
    except ValueError as e:
        # For debugging: don't leak private key or full seed, but include short hint
        preview = (seed or "")[:120].replace("\n", "\\n")
        return jsonify({"error": f"TOTP generation failed: {e}", "seed_preview": preview}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error generating TOTP: {e}"}), 500

if __name__ == "__main__":
    # Dev server (not for production)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
