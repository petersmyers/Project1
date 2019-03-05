import csv
import pandas as pd
import os

file = "cleaned_hospital_data.csv"
hospital_data_df = pd.DataFrame(pd.read_csv(file))

# print(hospital_data_df.head())

columns = ["List_ID", "Hospital Name", "Rating", "Rating Count"]
hospital_data_df.drop(columns, axis=1, inplace=True)

# print(hospital_data_df.head())

hospital_data_df["Full Location"] = hospital_data_df["County"] + " " + hospital_data_df["State"]

# print(hospital_data_df.head())

result = hospital_data_df.groupby("Full Location").first()
# print(result.head())

result["Hospital Count"] = hospital_data_df["Full Location"].value_counts()
result.reset_index(inplace=True)

# print(result.head())
# print(hospital_data_df.head())

result = result.drop("Full Location", axis=1)

# print(result.head())

result.to_csv(r"number_of_hospitals_per_county.csv")