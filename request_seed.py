import requests

# Student Details - Double check these for typos!
student_id = "23MH1A05I0" 
repo_url = "https://github.com/Laharisrikotipalli/pki-2fa"

# Load public key as per Step 3 instructions
try:
    with open("student_public.pem", "r") as f:
        public_key_content = f.read()
except FileNotFoundError:
    print("Error: student_public.pem missing.")
    exit()

payload = {
    "student_id": student_id,
    "repo_url": repo_url,
    "public_key": public_key_content
}

# The specific endpoint from your image
url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Success! Encrypted Seed:", response.json().get("encrypted_seed"))
else:
    print(f"Error {response.status_code}: {response.text}")