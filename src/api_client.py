import requests
import os
import json
import csv
import pandas as pd
from dotenv import load_dotenv
from datetime import date

load_dotenv()
year = input("What year?:    ")
api_key = os.getenv("RANSOMWARE_API_KEY")

url = "https://api-pro.ransomware.live/victims/?year=" + str(year)
headers = {
    "accept": "application/json",
    "X-API-KEY" : api_key
}

response = requests.get(url, headers=headers)


data = response.json() # extracting json content

records = data['victims'] # gets it to where we want
df = pd.json_normalize(records) # takes the victim records, flattens them, puts them into Data Frame
df_with_filters = df[['country', 'activity', 'attackdate', 'victim', 'group']]

df_with_filters.to_csv("ransowmare_victims-" + date.today().strftime("%Y-%m-%d") + '.csv', index=False)
