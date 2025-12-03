import base64
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-char hex seed → bytes → base32 string
    """
    # hex → bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # bytes → base32 (uppercase, no '=' padding)
    b32 = base64.b32encode(seed_bytes).decode('utf-8')

    return b32


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code (6 digits, SHA1, 30s)
    """
    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    return totp.now()     # string, e.g. "123456"


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify user-entered TOTP code with ±30s tolerance.
    valid_window=1 → accept previous/next step as well.
    """
    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    return totp.verify(code, valid_window=valid_window)
