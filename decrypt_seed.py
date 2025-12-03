from typing import Union
import base64, os
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.backends import default_backend

def _load_private_key_if_needed(private_key) -> RSAPrivateKey:
    if isinstance(private_key, RSAPrivateKey):
        return private_key
    if isinstance(private_key, str):
        private_key = private_key.encode("utf-8")
    if isinstance(private_key, (bytes, bytearray)):
        key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())
        if not isinstance(key, RSAPrivateKey):
            raise ValueError("Loaded key is not an RSA private key")
        return key
    raise ValueError("private_key must be RSAPrivateKey instance or PEM bytes/string")

def _validate_hex_seed(hexstr: str) -> None:
    if not isinstance(hexstr, str):
        raise ValueError("Decrypted seed is not a string")
    s = hexstr.strip().lower()
    if len(s) != 64:
        raise ValueError(f"Decrypted seed length invalid: expected 64 hex chars, got {len(s)}")
    if any(c not in "0123456789abcdef" for c in s):
        raise ValueError("Decrypted seed contains non-hex characters")

def decrypt_seed(encrypted_seed_b64: str, private_key: Union[RSAPrivateKey, bytes, str]) -> str:
    if not isinstance(encrypted_seed_b64, str):
        raise ValueError("encrypted_seed_b64 must be a base64 string")
    try:
        ciphertext = base64.b64decode(encrypted_seed_b64, validate=True)
    except Exception as e:
        raise ValueError(f"Invalid base64 encrypted_seed: {e}") from e

    key_obj = _load_private_key_if_needed(private_key)

    try:
        plaintext_bytes = key_obj.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise ValueError("RSA/OAEP decryption failed") from e

    try:
        plaintext = plaintext_bytes.decode("utf-8")
    except Exception as e:
        raise ValueError("Decrypted bytes are not valid UTF-8") from e

    hex_seed = plaintext.strip()
    _validate_hex_seed(hex_seed)
    hex_seed = hex_seed.lower()

    # write to DATA_DIR (env) or ./data by default
    data_dir = Path(os.environ.get("DATA_DIR", "./data"))
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        seed_path = data_dir / "seed.txt"
        seed_path.write_text(hex_seed + "\n", encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Decrypted seed validated but failed to write to {data_dir}/seed.txt: {e}") from e

    return hex_seed
