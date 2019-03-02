import json
import pandas as pd
import requests
import csv
from pandas.io.json import json_normalize

heart_df = pd.read_csv("./Heart_Disease_Mortality_Data_Among_US_Adults_35_by_State_Territory_and_County.csv")

print(heart_df.head())

# print(heart_df.count())

heart_county_df = heart_df[heart_df["GeographicLevel"]=="County"]

print(heart_county_df.head())

# print(heart_county_df.count())

heart_county_df = heart_county_df.head()
base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

target_type = "hospitals"
gkey = "AIzaSyDIIaLDgFwpgQTpp17XxShP57DDhF3WoUg"

heart_county_json_df = pd.DataFrame(columns=["County", "JSON_Data"])

print(heart_county_json_df.head())

for index, row in heart_county_df.iterrows():
    target_county = row["LocationDesc"]
    target_county.replace(" ", "+")
    params = {
        "query": "f{target_type}s+in+{target_county}+county",
        "key": gkey
    }

    county_json_data = requests.get(base_url, params=params)

    print(county_json_data)

    county_json_data = county_json_data.json()

    print(county_json_data)

    # county_json_data_df = pd.DataFrame.from_dict(json_normalize(county_json_data), orient="columns")
    # print(county_json_data_df.head())
    # try:
    #     heart_county_json_df.loc[index, "County"] = target_county
    #     heart_county_json_df.loc[index, "JSON_Data"] = county_json_data_df["name"]
    # except (KeyError, IndexError):
    #     print("Well fuck")

# print(heart_county_json_df["JSON_Data"])