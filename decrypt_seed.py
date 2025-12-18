import base64
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64, private_key):
    # Decode the base64 input string back into bytes
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    
    # Decrypt using RSA PKCS1v15 padding
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15()
    )
    
    # Convert the raw bytes into a hex string for safe storage
    return decrypted_bytes.hex()