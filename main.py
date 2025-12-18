from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from decrypt_seed import decrypt_seed
from totp import generate_totp_code, verify_totp_code
import time
import os

app = FastAPI()
DATA_PATH = Path("/data/seed.txt")

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
def api_decrypt_seed(req: DecryptRequest):
    try:
        # 1. Open the key (Filename is correct now)
        with open("student_private.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        # 2. Decrypt using your existing function
        seed = decrypt_seed(req.encrypted_seed, private_key)

        # 3. Save it to /data/seed.txt
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_PATH, "w") as f:
            f.write(seed)
        
        # 4. Crucial for Step 11 & 12: Make file readable by Cron/Restarts
        os.chmod(DATA_PATH, 0o666) 

        return {"status": "ok"}
    except Exception as e:
        # This will show you exactly WHAT failed in 'docker logs'
        print(f"Decryption failed: {e}") 
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/generate-2fa")
def api_generate_2fa():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    hex_seed = DATA_PATH.read_text().strip()
    code = generate_totp_code(hex_seed)
    return {"code": code, "valid_for": 30 - (int(time.time()) % 30)}

@app.post("/verify-2fa")
def api_verify_2fa(req: VerifyRequest):
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    hex_seed = DATA_PATH.read_text().strip()
    is_valid = verify_totp_code(hex_seed, req.code)
    return {"valid": is_valid}