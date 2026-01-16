import requests

# Student Details
student_id = "23MH1A05I0"
# Ensure this matches your public repo exactly
github_repo_url = "https://github.com/Laharisrikotipalli/pki-2fa" 

# Read your public key (Step 3 Requirement)
try:
    with open("student_public.pem", "r") as f:
        public_key_content = f.read()
except FileNotFoundError:
    print("Error: student_public.pem not found.")
    exit()

# Updated payload with 'github_repo_url'
payload = {
    "student_id": student_id,
    "github_repo_url": github_repo_url,
    "public_key": public_key_content
}

# The specific endpoint from your instructions
url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print("Successfully received seed!")
    print("Encrypted Seed:", data.get("encrypted_seed"))
else:
    print(f"Error {response.status_code}: {response.text}")