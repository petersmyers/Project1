import json
import pandas as pd
import requests
import csv
import io
from pandas.io.json import json_normalize

heart_df = pd.read_csv("./Heart_Disease_Mortality_Data_Among_US_Adults_35_by_State_Territory_and_County.csv")

# print(heart_df.head())

# print(heart_df.count())

heart_county_only_df = heart_df[heart_df["GeographicLevel"]=="County"]

# print(heart_county_df.head())

# print(heart_county_df.count())

# heart_county_only_df = heart_county_only_df.head()
base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

target_type = "hospitals"
gkey = input("Enter an API key. ")

rating = []
rating_count = []
hospital_name = []
county = []
state = []

for index, row in heart_county_only_df.iterrows():
    target_county = row["LocationDesc"]
    target_county.replace(" ", "+")
    target_state = row["LocationAbbr"]
    params = {
        "query": f"{target_type}+in+{target_county},+{target_state}",
        "key": gkey
    }

    response = requests.get(base_url, params=params).json()
    
    for i in range(len(response["results"])):
        rating.append(response["results"][i]["rating"])
        rating_count.append(response["results"][i]["user_ratings_total"])
        hospital_name.append(response["results"][i]["name"])
        county.append(row["LocationDesc"])
        state.append(row["LocationAbbr"])
    
# print(len(rating))
# print(rating)
# print(len(rating_count))
# print(rating_count)
# print(len(hospital_name))
# print(hospital_name)
# print(len(county))
# print(county)
# print(len(state))
# print(state)

data = {"County": county, "State": state, "Hospital Name": hospital_name, "Rating": rating, "Rating Count": rating_count}
hospital_data_df = pd.DataFrame(data, columns=["County", "State", "Hospital Name", "Rating", "Rating Count"])

hospital_data_df.to_csv(r"cleaned_hospital_data.csv")