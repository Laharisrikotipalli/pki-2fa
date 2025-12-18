import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def test_decryption():
    try:
        # 1. Load the private key (This is where you failed Step 1)
        with open("student_private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        print("✅ SUCCESS: Private Key loaded (Step 1 markers removed).")

        # 2. Simulate the Decryption logic (This is Step 6)
        # We'll use the public key to make a test message
        public_key = private_key.public_key()
        message = b"test_seed_123"
        
        # Encrypting to test
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypting (The logic you need in main.py)
        decrypted = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        if decrypted == message:
            print("✅ SUCCESS: Decryption logic works with OAEP-SHA256.")
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        print("\nPossible fix: Check for '<<<<' in your pem file or update your padding to OAEP-SHA256.")

if __name__ == "__main__":
    test_decryption()