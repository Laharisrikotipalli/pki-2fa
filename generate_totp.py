from decrypt_seed import decrypt_seed
from pathlib import Path

# load encrypted seed and private key
enc = Path("encrypted_seed.txt").read_text().strip()
priv = Path("student_private.pem").read_bytes()

hex_seed = decrypt_seed(enc, priv)   # returns 64-char hex string
# convert hex -> base32 for pyotp
import base64
b = bytes.fromhex(hex_seed)
b32 = base64.b32encode(b).decode('utf-8').strip('=')
import pyotp
print(pyotp.TOTP(b32).now())
