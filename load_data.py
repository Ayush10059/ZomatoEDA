import os
import numpy as np
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim

path = "data/locations.csv"

@st.cache
def get_data():
    df = pd.read_csv("data/zomato.csv")
    return df

df = get_data()

def load_location():
    if (os.path.exists(path) == False):
        locations=pd.DataFrame({"Name":df['location'].unique()})
        locations['Name']=locations['Name'].apply(lambda x: "Bangalore " + str(x))
        lat_lon=[]
        lat=[]
        lon=[]
        geolocator=Nominatim(user_agent="app")
        for location in locations['Name']:
            location = geolocator.geocode(location)
            if location is None:
                lat.append(np.nan)
                lon.append(np.nan)
                lat_lon.append(np.nan)
            else:    
                lat.append(location.latitude)
                lon.append(location.longitude)
                geo=(location.latitude, location.longitude)
                lat_lon.append(geo)

        locations['geo_loc']=lat_lon
        locations['lat']=lat
        locations['lon']=lon
        locations.to_csv('data/locations.csv',index=False)
    
    else:
        locations = pd.read_csv("data/locations.csv")
    return locations
