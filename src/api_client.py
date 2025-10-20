import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("RANSOMWARE_API_KEY")

url = "https://api-pro.ransomware.live/victims/"
headers = {
    "accept": "application/json",
    "X-API-KEY" : api_key
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json()[0])  # testing to see if it works. should pull first record
