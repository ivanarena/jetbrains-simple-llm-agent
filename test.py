import requests

url = "http://localhost:8000/agent"
data = {"msg": "What directory are you in?"}

response = requests.post(url, json=data)
print(response.json())
