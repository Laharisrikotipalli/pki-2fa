from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_rsa_keypair(key_size: int = 4096):
    """
    Generates an RSA key pair with 4096 bits and public exponent 65537.

    Returns:
        Tuple of (private_key, public_key) objects from cryptography library.
    """
    # Key size: 4096 bits
    # Public exponent: 65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    return private_key, private_key.public_key()

def save_keypair(private_key, public_key, private_path, public_path):
    """
    Serializes and saves the private and public keys to PEM files.
    """
    # 1. Save Private Key (PKCS8 format, unencrypted)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(private_path, "wb") as f:
        f.write(private_pem)
    
    # 2. Save Public Key (SubjectPublicKeyInfo format)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(public_path, "wb") as f:
        f.write(public_pem)

# --- Execution ---
if __name__ == "__main__":
    PRIVATE_KEY_FILE = "student_private.pem"
    PUBLIC_KEY_FILE = "student_public.pem"

    print("Starting RSA 4096-bit key pair generation...")
    private_key, public_key = generate_rsa_keypair(key_size=4096)
    
    # Save the keys with the required filenames
    save_keypair(private_key, public_key, PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)
    
    print(f"Key generation complete.")
    print(f"Private Key saved to: {PRIVATE_KEY_FILE} (REQUIRED to commit)")
    print(f"Public Key saved to: {PUBLIC_KEY_FILE} (REQUIRED to commit)")
    print("\nIMPORTANT: Commit both files to your Git repository now.")
