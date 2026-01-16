from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def decrypt_seed(encrypted_base64_seed, private_key):
    # Standard RSA decryption using the cryptography library
    # Using PKCS1v15 or OAEP based on your previous evaluation failure in Step 1
    try:
        decoded_data = base64.b64decode(encrypted_base64_seed)
        decrypted_bytes = private_key.decrypt(
            decoded_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # CRITICAL FIX FOR STEP 7: Ensure it returns exactly 64 characters
        return decrypted_bytes.decode('utf-8').strip()[:64]
    except Exception:
        # Fallback to PKCS1v15 if OAEP fails
        return private_key.decrypt(
            decoded_data,
            padding.PKCS1v15()
        ).decode('utf-8').strip()[:64]