# Code for census pulling

# **********************************************
# Don't forget to jump into PythonData
# **********************************************

# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from census import Census
import gmaps
import time

# Census & gmaps API Keys
census_api = input("What's your Census API key?")
gmap_api = input ("What's your Gmaps API key?")

c = Census(census_api, year=2014)


# Configure gmaps
# gmaps.configure(api_key=gkey)

# Run Census Search to retrieve data on all zip codes (2013 ACS5 Census)
# See: https://github.com/CommerceDataService/census-wrapper for library documentation
# See: https://gist.github.com/afhaque/60558290d6efd892351c4b64e5c01e9b for labels
census_data = c.acs5.get(("NAME", "B17001A_002E", "B17001B_002E", "B17001C_002E",
                          "B17001D_002E","B17001E_002E", "B17001G_002E", 
                          "B17001I_002E", "B01003_001E"),{'for': 'county:*'})

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
                                        "B01003_001E" : "totalpop",
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
census_pd["white_rate"] = 100 * (census_pd["poverty_White"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["black_rate"] = 100 * (census_pd["poverty_Black"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["amerind_rate"] = 100 * (census_pd["poverty_AmerInd"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["asian_rate"] = 100 * (census_pd["poverty_Asian"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["nathaw_rate"] = 100 * (census_pd["poverty_NatHaw"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["multi_rate"] = 100 * (census_pd["poverty_Multi"].astype(int) / census_pd["totalpop"].astype(int))
census_pd["hisp_rate"] = 100 * (census_pd["poverty_Hisp"].astype(int) / census_pd["totalpop"].astype(int))


### Heat Mapping?
# Configure gmaps with API key
gmaps.configure(api_key=gmap_api)
# Store 'Lat' and 'Lng' into  locations 
locations = county[["Lat", "Lng"]].astype(float)

# locations = (1,2)

# Convert Poverty Rate to float and store
# HINT: be sure to handle NaN values
poverty_rate_white = census_pd["white_rate"].astype(float)
# poverty_rate_white = census_pd["white_rate"][1].astype(float)

# Create a poverty Heatmap layer
white_povmap = gmaps.figure()

heat_layer_white = gmaps.heatmap_layer(locations, weights=poverty_rate_white, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

# Adjust heat_layer setting to help with heatmap dissipating on zoom
heat_layer_white.dissipating = False
heat_layer_white.max_intensity = 100
heat_layer_white.point_radius = 1

white_povmap.add_layer(heat_layer_white)

white_povmap