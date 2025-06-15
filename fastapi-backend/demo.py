import requests

# URL of your FastAPI signup endpoint
url = "http://localhost:8000/signup"

# Sample user data (modify this as needed)
payload = {
    "username": "admin1",
    "email": "admin1@example.com",
    "password": "adminpass123",
    "role": "admin",  # or "user"
    "security_code": "#@#@1289tony"  # Required only for admin
}

# Send POST request
response = requests.post(url, json=payload)

# Show server response
print("Status Code:", response.status_code)
print("Response:", response.json())
