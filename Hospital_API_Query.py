import json
import pandas as pd
import requests
import csv
import io
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
gkey = input("Enter an API key. ")

heart_county_json_df = pd.DataFrame(columns=["County", "JSON_Data"])

print(heart_county_json_df.head())

for index, row in heart_county_df.iterrows():
    target_county = row["LocationDesc"]
    target_county.replace(" ", "+")
    target_state = row["LocationAbbr"]
    params = {
        "query": f"{target_type}+in+{target_county},+{target_state}",
        "key": gkey
    }

    county_json_data = requests.get(base_url, params=params)

    # print(county_json_data)

    county_json_data = county_json_data.json()
    
    # with open("data.txt", "w") as f:
    #     f.write(json.dumps(county_json_data, indent = 4, sort_keys = True))

    county_json_data_df = pd.DataFrame.from_dict(json_normalize(county_json_data["results"]), orient="columns")
    print(county_json_data_df.head())
#     for items in 
#     try:
#         heart_county_json_df.loc[index, "County"] = target_county
#         heart_county_json_df.loc[index, "JSON_Data"] = county_json_data_df["results"]["name"]
#     except (KeyError, IndexError):
#         print("Well fuck")
# with open("data.txt", "w") as f:
#     f.write(heart_county_json_df["JSON_Data"])