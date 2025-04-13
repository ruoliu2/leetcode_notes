import requests
import json

url = "https://api.example.com/endpoint"
data = {"key": "value"}
headers = {"Content-Type": "application/json"}

# Making a POST request
response = requests.post(url, data=json.dumps(data), headers=headers)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print("Response JSON:", result)
else:
    print("Error:", response.status_code, response.text)
