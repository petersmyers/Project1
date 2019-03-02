import os
import csv
import pandas as pd

# Create Data
file = "Data.csv"
df = pd.read_csv(file)

# Deleting Colummns 
df = df.drop(columns= ["Year", "GeographicLevel","DataSource","Class",'Topic',"Data_Value_Type",'Data_Value_Footnote_Symbol','Data_Value_Footnote','StratificationCategory1','StratificationCategory2','TopicID','LocationID','Location 1','Data_Value_Unit'])
# Renaming Columns
df = df.rename(columns={"LocationAbbr": "State", "LocationDesc": "County", "Data_Value": "Value", "Stratification1": "Gender", "Stratification2": "Race/Ethnicity"})

# Dropping Rows that are empty
df = df.dropna(how='any')
#df.head(100)



# Sorting by county
county = pd.DataFrame(df)
county = county.loc[county['Gender']== "Overall"]
county = county.loc[county['Race/Ethnicity'] == "Overall"]
county = county.sort_values(['Value'],ascending=False)
#county.head()

# Sorting by Ethnicity (White)
white = pd.DataFrame(df)
white = white.loc[white['Gender']== "Overall"]
white = white.loc[white['Race/Ethnicity'] == "White"]
white = white.sort_values(['State'])
#white.head(100)

# Sorting by Ethnicity (Black)
black = pd.DataFrame(df)
black = black.loc[black['Gender']== "Overall"]
black = black.loc[black['Race/Ethnicity'] == "Black"]
black = black.sort_values(['State'])

# Sorting by Ethnicity (Hispanic)
hispanic = pd.DataFrame(df)
hispanic = hispanic.loc[hispanic['Gender']== "Overall"]
hispanic = hispanic.loc[hispanic['Race/Ethnicity'] == "Hispanic"]
hispanic = hispanic.sort_values(['State'])

# Sorting by Ethnicity (Indian)
Indian = pd.DataFrame(df)
Indian = Indian.loc[Indian['Gender']== "Overall"]
Indian = Indian.loc[Indian['Race/Ethnicity'] == "American Indian and Alaskan Native"]
Indian = Indian.sort_values(['State'])

# Sorting by Ethnicity (Asian)
Asian = pd.DataFrame(df)
Asian = Asian.loc[Asian['Gender']== "Overall"]
Asian = Asian.loc[Asian['Race/Ethnicity'] == "Asian and Pacific Islander"]
Asian = Asian.sort_values(['State'])