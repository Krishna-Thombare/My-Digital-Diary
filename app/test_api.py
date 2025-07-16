import requests

url = 'http://127.0.0.1:5000/chat'  # adjust if your server runs on a different port

data = {
    "message": "What is the capital of India?"
}

response = requests.post(url, json=data)

if response.ok:
    print("✅ Response:", response.json())
else:
    print("❌ Error:", response.status_code, response.text)
