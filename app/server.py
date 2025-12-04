from flask import Flask, request, jsonify
import os
import sys
import json

# project imports (use the relative imports you already had)
from .decrypt_seed import decrypt_seed      # decrypt_seed(encrypted_b64, private_key_bytes) -> plaintext seed (str)
from .totp_generator import generate_totp   # generate_totp(seed_str) -> 6-digit string

# debug print (kept from your original)
print("DEBUG: got request body:", file=sys.stderr)
##COMMENTED_BY_FIX print(json.dumps(request.get_json()), file=sys.stderr)
sys.stderr.flush()

# Flask app must be initialized BEFORE route decorators
app = Flask(__name__)

# Where the decrypted seed is stored (docker volume)
SEED_FILE = "/app/data/seed.txt"


# ---------------------------
#         HEALTH CHECK
# ---------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200


# ---------------------------
#     DECRYPT SEED ENDPOINT
# ---------------------------
@app.route("/decrypt-seed", methods=["POST"])
def decrypt_seed_route():
    """
    1. Read incoming encrypted seed (base64) from JSON body: {"encrypted_seed": "..."}
    2. Decrypt using student's private key (RSA-OAEP-SHA256)
    3. Save plaintext seed to SEED_FILE (/app/data/seed.txt)
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    encrypted_seed = data.get("encrypted_seed") if isinstance(data, dict) else None

    if not encrypted_seed:
        return jsonify({"error": "Missing encrypted_seed"}), 400

    # Load student private key (bytes)
    priv_path = "/app/keys/student_private.pem"
    if not os.path.isfile(priv_path):
        return jsonify({"error": "private key not found on server", "path": priv_path}), 500

    try:
        with open(priv_path, "rb") as f:
            private_key_bytes = f.read()
    except Exception as e:
        app.logger.exception("Failed to read private key: %s", e)
        return jsonify({"error": "failed to read private key", "detail": str(e)}), 500

    # Decrypt
    try:
        plaintext_seed = decrypt_seed(encrypted_seed, private_key_bytes)
    except Exception as e:
        app.logger.exception("Decryption failed: %s", e)
        return jsonify({"error": "Decryption failed", "detail": str(e)}), 400

    if not plaintext_seed:
        return jsonify({"error": "Decryption returned empty seed"}), 500

    # Ensure data folder exists and persist seed
    try:
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(plaintext_seed.strip())
    except Exception as e:
        app.logger.exception("Failed to write seed to disk: %s", e)
        return jsonify({"error": "failed to persist seed", "detail": str(e)}), 500

    return jsonify({"status": "ok", "message": "Seed decrypted and stored"}), 200


# ---------------------------
#         TOTP ENDPOINT
# ---------------------------
@app.route("/totp", methods=["GET"])
def totp_route():
    """
    Returns the current TOTP as JSON: {"totp": "123456"}.
    Order:
      1) Read plaintext seed from SEED_FILE (/app/data/seed.txt)
      2) Read /app/seed.txt
      3) Read /app/encrypted_seed.txt and decrypt using /app/keys/student_private.pem
    """
    alt_plain = "/app/seed.txt"
    enc_path = "/app/encrypted_seed.txt"
    priv_key_path = "/app/keys/student_private.pem"

    seed = None

    # 1) try SEED_FILE
    try:
        if os.path.isfile(SEED_FILE):
            with open(SEED_FILE, "r") as f:
                s = f.read().strip()
                if s:
                    seed = s
    except Exception as e:
        app.logger.debug("Could not read SEED_FILE: %s", e)

    # 2) try alt plaintext
    if not seed:
        try:
            if os.path.isfile(alt_plain):
                with open(alt_plain, "r") as f:
                    s = f.read().strip()
                    if s:
                        seed = s
        except Exception as e:
            app.logger.debug("Could not read alt_plain seed: %s", e)

    # 3) try encrypted seed + decrypt
    if not seed:
        try:
            if os.path.isfile(enc_path) and os.path.isfile(priv_key_path):
                with open(enc_path, "r") as f:
                    enc = f.read().strip()
                with open(priv_key_path, "rb") as f:
                    priv_bytes = f.read()
                plaintext = decrypt_seed(enc, priv_bytes)
                if plaintext:
                    seed = plaintext.strip()
                    # persist for future calls
                    try:
                        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
                        with open(SEED_FILE, "w") as f:
                            f.write(seed)
                    except Exception as e:
                        app.logger.debug("Failed to persist decrypted seed: %s", e)
        except Exception as e:
            app.logger.exception("Failed to decrypt encrypted_seed.txt: %s", e)
            return jsonify({"error": "failed to decrypt encrypted_seed", "detail": str(e)}), 500

    if not seed:
        return jsonify({"error": "seed not found; cannot generate TOTP"}), 500

    # generate totp using your existing generator
    try:
        code = generate_totp(seed)
        return jsonify({"totp": code}), 200
    except Exception as e:
        app.logger.exception("Failed to generate TOTP: %s", e)
        return jsonify({"error": "failed to generate totp", "detail": str(e)}), 500


# ---------------------------
#        MAIN GUARD
# ---------------------------
if __name__ == "__main__":
    # bind to 0.0.0.0 so the container port maps to host
    app.run(host="0.0.0.0", port=8080)
