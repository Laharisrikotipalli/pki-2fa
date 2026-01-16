import pyotp
import base64

def generate_totp_code(hex_seed):
    # Convert 64-char hex seed to base32 for pyotp
    seed_bytes = bytes.fromhex(hex_seed.strip()[:64])
    base32_secret = base64.b32encode(seed_bytes).decode('utf-8')
    
    totp = pyotp.TOTP(base32_secret)
    return totp.now()

def verify_totp_code(hex_seed, code):
    seed_bytes = bytes.fromhex(hex_seed.strip()[:64])
    base32_secret = base64.b32encode(seed_bytes).decode('utf-8')
    
    totp = pyotp.TOTP(base32_secret)
    return totp.verify(code)