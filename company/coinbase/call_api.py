import requests
import json

url = "https://api.example.com/endpoint"
data = {"key": "value"}
# path var use params, query body use json
# Making a POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print("Response JSON:", result)
else:
    print("Error:", response.status_code, response.text)
