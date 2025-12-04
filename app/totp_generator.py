# app/totp_generator.py
import base64
import binascii
import pyotp
from typing import Union

def _to_base32(seed: Union[str, bytes]) -> str:
    """
    Convert various seed encodings to a base32 string acceptable to pyotp.TOTP.
    Accepts:
      - base32 string (letters A-Z2-7, maybe with '=' padding)
      - hex string (0-9a-f)
      - raw bytes
    """
    if isinstance(seed, bytes):
        raw = seed
        # convert raw bytes to base32 without padding
        return base64.b32encode(raw).decode('utf-8').rstrip('=')
    seed = seed.strip()
    # detect base32 (letters and digits 2-7)
    try:
        # try decoding as base32 (allow padding)
        _ = base64.b32decode(seed.upper() + '=' * ((8 - len(seed) % 8) % 8))
        return seed.upper().rstrip('=')
    except Exception:
        pass
    # detect hex
    try:
        raw = binascii.unhexlify(seed)
        return base64.b32encode(raw).decode('utf-8').rstrip('=')
    except Exception:
        pass
    # fallback: treat as ASCII bytes
    return base64.b32encode(seed.encode('utf-8')).decode('utf-8').rstrip('=')

def generate_totp(seed: Union[str, bytes]) -> str:
    """
    Return a 6-digit TOTP code for the given seed.
    """
    b32 = _to_base32(seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30)  # RFC6238 defaults
    return totp.now()
