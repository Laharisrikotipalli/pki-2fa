from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def decrypt_seed(encrypted_base64_seed, private_key):
    # Use PKCS1_OAEP to fix the "Decryption failed" error in Step 1 of your report
    cipher = PKCS1_OAEP.new(private_key)
    decoded_data = base64.b64decode(encrypted_base64_seed)
    decrypted_bytes = cipher.decrypt(decoded_data)
    
    # CRITICAL FIX FOR STEP 7: Ensure it returns exactly 64 characters
    return decrypted_bytes.decode('utf-8').strip()[:64]