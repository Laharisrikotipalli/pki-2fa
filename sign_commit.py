import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# 1. Update this with your latest commit hash (Step 2 below)
commit_id = "de47f1f62815fe8ad1be4257bfad61c3a93a443f".strip()

def sign_my_commit():
    try:
        # 2. Use your ACTUAL key filename
        with open("student_private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None  # Change if your key has a password
            )

        # 3. Sign the commit ID using PKCS1v15 padding
        signature = private_key.sign(
            commit_id.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        # 4. Save as Base64 for the evaluator
        with open("commit_proof.txt", "wb") as f:
            f.write(base64.b64encode(signature))

        print(f"✅ Successfully signed commit: {commit_id}")
        print("✅ commit_proof.txt is ready.")

    except FileNotFoundError:
        print("❌ Error: Could not find student_private.pem in this folder.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sign_my_commit()