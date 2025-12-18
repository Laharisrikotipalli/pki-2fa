import pyotp
import time

def decrypt_seed(filepath):
    # TODO: Replace this logic with your actual decryption code
    # For example, if you're using a library like 'cryptography'
    with open(filepath, "r") as f:
        encrypted_data = f.read()
    
    # Placeholder: Assuming 'secret' is the result after decryption
    # secret = some_decryption_function(encrypted_data)
    return encrypted_data.strip() # Returning raw data for now

def run_test():
    try:
        # 1. Decrypt the seed
        secret = decrypt_seed("encrypted_seed.txt")
        
        # 2. Initialize the TOTP object
        totp = pyotp.TOTP(secret)
        
        # 3. Generate the code
        generated_code = totp.now()
        
        # 4. Verify the code
        is_valid = totp.verify(generated_code)
        
        # Output result
        print(f"Generated TOTP: {generated_code}")
        print(f"Is Valid: {is_valid}")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    run_test()