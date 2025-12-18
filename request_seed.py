import requests
from pathlib import Path

def request_seed():
    API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
    STUDENT_ID = "23MH1A05I0"
    GITHUB_REPO_URL = "https://github.com/Laharisrikotipalli/pki-2fa"
    OUTPUT_FILE = "encrypted_seed.txt"
    
    # Use the exact PEM format with actual newlines
    public_key = (
        "-----BEGIN PUBLIC KEY-----\n"
        "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA0IOy8td5faYy4sZDaqAQ\n"
        "c460+zfa6R58gywRfWqIsPSjmUKHbFAwgcMtEzyIvwnNxXpg6Xxo5/N4iiPnvrnQ\n"
        "mI+1dXopoa34+FkCq7JWMeGt/QfdW8P7akH1ewtbCrnBUriQ/qSImlzOD3mX1vYJ\n"
        "CsyS1GeAH3m6VJNtB5oNX7M9Of6r1y5xy4ethWiw4uHpsbR2o+znGB/8HF4HTvDE\n"
        "ziBOxoyJutKA7yll/677s2lPk9Ohf4cyNl/mAt7WKqXVZaOwNC0+SQAww4NXvTwJ\n"
        "EL63ZHr5fDMGwPp5cgMMVwM8JfbToYZCzbtLaQJKR5qZQs6X89Tp+0lbLRk0ntAQ\n"
        "5PXJ0xmFtsv2ZqZvJNg8TkzT/q/gUnZV8Mmjmj5uS1g/Z6bfJkLz9e9zOz6kt7c0\n"
        "RpHlgtqTb2/c6vghKXW33AXMdVMghVrUIGkjAheouZV5bLaQ12k6yNzWlPfWRhQg\n"
        "YzNXsPFl0REytXvXg2yaUobdy1XKBGD7y5ZmJODmAiUOWXwWCRSNfOxYhpQDSo5m\n"
        "Yhx+0oG9/INx+BvzmTF3Vm2FA1JLj8yaWLI4BPO9vjgF/D4VSoAVGhKwDw9zwRE/\n"
        "hwy56Y+FEVWYjLfFbcurSMaNAfSf2BYK8HgzMkSd3ex4biPrnLOI1GYvDrGeD1XN\n"
        "gkkZ35/yQNQTgl2+AnHCpscCAwEAAQ==\n"
        "-----END PUBLIC KEY-----"
    )

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key  # Send the string with actual newlines
    }

    print(f"Requesting seed for {STUDENT_ID}...")
    # Using json=payload will automatically handle the newline escaping correctly
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        seed = data.get("encrypted_seed")
        Path(OUTPUT_FILE).write_text(seed)
        print(f"✅ Success! Seed saved to {OUTPUT_FILE}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response Body: {response.text}")

if __name__ == "__main__":
    request_seed()