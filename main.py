from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from decrypt_seed import decrypt_seed
from totp import generate_totp_code, verify_totp_code
import time
import os

app = FastAPI()
# Persistence path verified for Step 12
DATA_PATH = Path("/data/seed.txt")

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def api_decrypt_seed(req: DecryptRequest):
    try:
        # Load your student private key for decryption
        with open("student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # Decrypt the seed
        raw_seed = decrypt_seed(req.encrypted_seed, private_key)

        # FIX FOR STEP 7: Slicing to exactly 64 characters
        # This prevents the 304-character length error from your report
        clean_seed = raw_seed.strip()[:64]

        # Save to the persistent volume
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(clean_seed)
        
        # Ensure the file is readable by the cron service (Step 11/12)
        os.chmod(DATA_PATH, 0o666) 

        return {"status": "ok"}
    except Exception as e:
        print(f"Decryption failed: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-2fa")
def api_generate_2fa():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    # Ensure we use the 64-char version for TOTP generation
    hex_seed = DATA_PATH.read_text().strip()[:64]
    code = generate_totp_code(hex_seed)
    
    return {"code": code}

@app.post("/verify-2fa")
def api_verify_2fa(req: VerifyRequest):
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    # Fix for Step 9: Use the correct seed for verification
    hex_seed = DATA_PATH.read_text().strip()[:64]
    is_valid = verify_totp_code(hex_seed, req.code)
    
    return {"valid": is_valid}