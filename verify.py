from cryptography.hazmat.primitives import serialization

def check_key():
    try:
        with open("student_private.pem", "rb") as f:
            key_data = f.read()
            # This attempts to load the key just like the evaluator does
            serialization.load_pem_private_key(key_data, password=None)
        print("✅ SUCCESS: Your student_private.pem is CLEAN and valid.")
    except Exception as e:
        print("❌ FAIL: Your key is still invalid.")
        print(f"ERROR MESSAGE: {e}")
        print("\nACTION: Open student_private.pem and delete any lines containing '<<<<', '====', or '>>>>'.")

if __name__ == "__main__":
    check_key()