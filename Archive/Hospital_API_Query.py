import os
import csv
import pandas as pd
import json
import requests

#Importing and Reading csv
file = "countydata.csv"
county_df = pd.read_csv(file)

print(county_df.head())

base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

target_type = "hospital"
gkey = input("Enter an API key. ")

rating = []
rating_count = []
hospital_name = []
county_name = []
state_name = []

for index, row in county_df.iterrows():
    target_county = row["County"]
#     target_county.replace(" ", "+")
    target_state = row["State"]
    params = {
        "query": f"{target_county}, {target_state}",
        "type": target_type,
        "key": gkey
    }
    
    response = requests.get(base_url, params=params).json()
    
    for i in range(len(response["results"])):
        rating.append(response["results"][i]["rating"])
        rating_count.append(response["results"][i]["user_ratings_total"])
        hospital_name.append(response["results"][i]["name"])
        county_name.append(row["County"])
        state_name.append(row["State"])

data = {"County": county_name, "State": state_name, "Hospital Name": hospital_name, "Rating": rating, "Rating Count": rating_count}
hospital_data_df = pd.DataFrame(data, columns=["County", "State", "Hospital Name", "Rating", "Rating Count"])

hospital_data_df.to_csv(r"cleaned_hospital_data.csv")