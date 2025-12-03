from flask import Flask, request, jsonify
import os
import base64
from datetime import datetime
from pathlib import Path

from decrypt_seed import decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code

app = Flask(__name__)

DATA_FILE = "data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"


def load_hex_seed():
    """Load the decrypted seed from disk."""
    if not os.path.exists(DATA_FILE):
        return None
    return Path(DATA_FILE).read_text().strip()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# -----------------------------------------------------------
# 1️⃣ POST /decrypt-seed
# -----------------------------------------------------------

@app.route("/decrypt-seed", methods=["POST"])
def api_decrypt_seed():
    try:
        data = request.get_json()
        if not data or "encrypted_seed" not in data:
            return jsonify({"error": "Missing encrypted_seed"}), 400

        encrypted_seed_b64 = data["encrypted_seed"]

        # Load private key
        if not os.path.exists(PRIVATE_KEY_FILE):
            return jsonify({"error": "Private key not found"}), 500

        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key_bytes = f.read()

        try:
            hex_seed = decrypt_seed(encrypted_seed_b64, private_key_bytes)
        except Exception as e:
            return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

        Path("data").mkdir(exist_ok=True)
        Path(DATA_FILE).write_text(hex_seed)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


# -----------------------------------------------------------
# 2️⃣ GET /generate-2fa
# -----------------------------------------------------------

@app.route("/generate-2fa", methods=["GET"])
def api_generate_2fa():
    try:
        hex_seed = load_hex_seed()
        if hex_seed is None:
            return jsonify({"error": "Seed not decrypted yet"}), 500

        code = generate_totp_code(hex_seed)

        now = int(datetime.utcnow().timestamp())
        valid_for = 30 - (now % 30)

        return jsonify({
            "code": code,
            "valid_for": valid_for
        }), 200

    except Exception as e:
        return jsonify({"error": f"TOTP generation failed: {str(e)}"}), 500


# -----------------------------------------------------------
# 3️⃣ POST /verify-2fa
# -----------------------------------------------------------

@app.route("/verify-2fa", methods=["POST"])
def api_verify_2fa():
    try:
        data = request.get_json()
        if not data or "code" not in data:
            return jsonify({"error": "Missing code"}), 400

        code = data["code"]

        hex_seed = load_hex_seed()
        if hex_seed is None:
            return jsonify({"error": "Seed not decrypted yet"}), 500

        is_valid = verify_totp_code(hex_seed, code)

        return jsonify({"valid": is_valid}), 200

    except Exception as e:
        return jsonify({"error": f"Verification failed: {str(e)}"}), 500


# -----------------------------------------------------------
# Run server
# -----------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
