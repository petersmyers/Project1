# Code for census pulling
# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from census import Census
import gmaps
import time

# Census & gmaps API Keys
# census_api = input("What's your Census API key?")
census_api = "85ac64b6b5a9c0901b00329d1ef41f0c53ccfc98"
c = Census(census_api, year=2014)

# Configure gmaps
# gmaps.configure(api_key=gkey)

# Run Census Search to retrieve data on all zip codes (2013 ACS5 Census)
# See: https://github.com/CommerceDataService/census-wrapper for library documentation
# See: https://gist.github.com/afhaque/60558290d6efd892351c4b64e5c01e9b for labels
census_data = c.acs5.get(("NAME", "B17001A_002E", "B17001B_002E", "B17001C_002E",
                          "B17001D_002E","B17001E_002E", "B17001G_002E", "B17001I_002E"),
                           {'for': 'county:*'})

# Convert to DataFrame
census_pd = pd.DataFrame(census_data)
census_pd

# Column Reordering
census_pd = census_pd.rename(columns={"B17001A_002E": "poverty_White", 
                                        "B17001B_002E": "poverty_Black", 
                                        "B17001C_002E": "poverty_AmerInd",
                                        "B17001D_002E": "poverty_Asian",
                                        "B17001E_002E": "poverty_NatHaw", 
                                        "B17001G_002E": "poverty_Multi", 
                                        "B17001I_002E": "poverty_Hisp",
                                          "NAME": "Name", "county": "Country"})

# Divide the "name" into its county and state separately. 
census_pd["CountyName"] = ""
census_pd["StateName"] = ""
for i in range(0,len(census_pd)):
    st = census_pd.Name[i].split(",")
    ct = st[0].split("County")
    census_pd.CountyName[i] = ct[0]
    census_pd.StateName[i] = st[1]
# Add in Poverty Rate (Poverty Count / Population)
census_pd["Poverty Rate"] = 100 * \
    census_pd["Poverty Count"].astype(
        int) / census_pd["Population"].astype(int)

# Final DataFrame
census_pd = census_pd[["Zipcode", "Population", "Median Age", "Household Income",
                       "Per Capita Income", "Poverty Count", "Poverty Rate"]]

# Visualize
print(len(census_pd))
census_pd.head()


### Heat Mapping?
# Configure gmaps with API key
gmaps.configure(api_key=gkey)
# Store 'Lat' and 'Lng' into  locations 
locations = census_data_complete[["Lat", "Lng"]].astype(float)

# Convert Poverty Rate to float and store
# HINT: be sure to handle NaN values
poverty_rate = census_data_complete["Poverty Rate"].astype(float)

# Create a poverty Heatmap layer
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=poverty_rate, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

# Adjust heat_layer setting to help with heatmap dissipating on zoom
heat_layer.dissipating = False
heat_layer.max_intensity = 100
heat_layer.point_radius = 1

fig.add_layer(heat_layer)

fig