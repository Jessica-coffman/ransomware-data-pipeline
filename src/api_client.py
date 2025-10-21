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
project_id = os.getenv("PROJECT_ID")
table_name = os.getenv("TABLE_NAME")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key
todays_year = int(date.today().strftime('%Y'))

if int(year) >= 2022 and int(year) <= todays_year:

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

    df_with_filters.to_csv("ransomware_victims_" + year + '.csv', index=False) # saves CSV

    #import into GCP 
    try:
        table_id = project_id + '.' + table_name + '.ransomware_victims_' + year
        client = bigquery.Client()
        upload = client.load_table_from_dataframe(df_with_filters, table_id)
        upload.result()
        print(f"uploaded {len(df_with_filters)} rows to {table_id}")
    except Exception as e:
        print("Error: ", e)
else:
    print('Error: year out of bounds')
