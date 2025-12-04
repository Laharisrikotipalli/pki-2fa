from flask import Flask, request, jsonify
from decrypt_seed import decrypt_seed
from totp_generator import generate_totp

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "OK"})

@app.post("/generate-2fa")
def generate_2fa():
    data = request.get_json()
    encrypted_seed = data.get("encrypted_seed")
    private_key = open("keys/student_private.pem", "rb").read()

    seed_hex = decrypt_seed(encrypted_seed, private_key)
    totp_code = generate_totp(seed_hex)

    return jsonify({"code": totp_code})

@app.post("/validate-2fa")
def validate_2fa():
    data = request.get_json()
    encrypted_seed = data.get("encrypted_seed")
    provided_code = data.get("code")

    private_key = open("keys/student_private.pem", "rb").read()
    seed_hex = decrypt_seed(encrypted_seed, private_key)
    expected_code = generate_totp(seed_hex)

    return jsonify({"valid": provided_code == expected_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
