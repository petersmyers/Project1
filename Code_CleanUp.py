import os
import csv
import pandas as pd

#Importing and Reading csv
file = "Data.csv"
df = pd.read_csv(file)

# Deleting Useless Columns
df = df.drop(columns= ["Year", "GeographicLevel","DataSource","Class",'Topic',"Data_Value_Type",'Data_Value_Footnote_Symbol','Data_Value_Footnote','StratificationCategory1','StratificationCategory2','TopicID','LocationID','Data_Value_Unit'])
df = df.rename(columns={"LocationAbbr": "State", "LocationDesc": "County", "Data_Value": "Value", "Stratification1": "Gender", "Stratification2": "Race/Ethnicity", "Location 1": "LatLng"})

# Dropping Rows that are empty
df = df.dropna(how='any')

# Getting 10% of dataframe
a = len(df)
rows = .1 *a
rows
#df.head()

#Cleaning Up LatLng Columns
split = df["LatLng"].str.split("(", n = 1, expand = True) 
split = split[1].str.split(", ", n = 1, expand = True) 
splitLng = split[1].str.split(")", n = 1, expand = True) 
# making seperate first name column from new data frame 
df["Lat"]= split[0] 
  
# making seperate last name column from new data frame 
df["Lng"]= splitLng[0] 
  
# Dropping old Name columns 
df.drop(columns =["LatLng"], inplace = True) 
#df.head() 


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

#Sorting Top 10%
top10 = county.iloc[range(0,round(rows)),]
top10.head()

#Sorting Bottom 10%
bottom10= county.iloc[range(len(county)- round(rows), len(county))]
bottom10.head()

# Top 10% for each Race/Ethnicity
white_top10 = pd.DataFrame()
black_top10 = pd.DataFrame()
hispanic_top10 = pd.DataFrame()
Asian_top10 = pd.DataFrame()
Indian_top10 = pd.DataFrame()
for i in top10['County']:
    sorted_white = white.loc[white['County'] == i]
    white_top10 = white_top10.append(sorted_white)
    
    sorted_black = black.loc[black['County'] == i]
    black_top10 = black_top10.append(sorted_black)
    
    his = hispanic.loc[hispanic['County'] == i]
    hispanic_top10 = hispanic_top10.append(his)
    
    asian = Asian.loc[Asian['County'] == i]
    Asian_top10 = Asian_top10.append(asian)
    
    In = Indian.loc[Indian['County'] == i]
    Indian_top10 = Indian_top10.append(In)

#Bottom 10 for each Race/Ethnicity
white_b10 = pd.DataFrame()
black_b10 = pd.DataFrame()
hispanic_b10 = pd.DataFrame()
Asian_b10 = pd.DataFrame()
Indian_b10 = pd.DataFrame()
for i in top10['County']:
    sorted_white = white.loc[white['County'] == i]
    white_b10 = white_b10.append(sorted_white)
    
    sorted_black = black.loc[black['County'] == i]
    black_b10 = black_b10.append(sorted_black)
    
    his = hispanic.loc[hispanic['County'] == i]
    hispanic_b10 = hispanic_b10.append(his)
    
    asian = Asian.loc[Asian['County'] == i]
    Asian_b10 = Asian_b10.append(asian)
    
    In = Indian.loc[Indian['County'] == i]
    Indian_b10 = Indian_b10.append(In)