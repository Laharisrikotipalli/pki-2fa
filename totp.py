import pyotp
import base64

def generate_totp_code(hex_seed):
    # Convert hex string back to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    # TOTP library requires base32
    b32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(b32_seed)
    return totp.now()

def verify_totp_code(hex_seed, code):
    # This function was missing, causing the ImportError
    seed_bytes = bytes.fromhex(hex_seed)
    b32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(b32_seed)
    return totp.verify(code)