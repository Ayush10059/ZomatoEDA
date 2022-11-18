import numpy as np
import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static 
from tqdm import tqdm
import re

from load_data import get_data 
from load_data import load_location 

df = get_data()

def map_page():

    st.sidebar.header("Please Filter Here:")

    listed_in_type = st.sidebar.multiselect(
        "Select Restaurant Type:",
        options=df["listed_in(type)"].unique(),
        # default=df["listed_in(type)"].unique(),
    )

    df_selection = df.query(
        "`listed_in(type)` == @listed_in_type"
    )

    locations = load_location()

    locations["Name"] = locations['Name'].apply(lambda x :  x.replace("Bangalore","")[1:])    
    
    Rest_locations = pd.DataFrame(df_selection['location'].value_counts().reset_index())
    Rest_locations.columns = ['Name','count']
    Rest_locations = Rest_locations.merge(locations,on='Name',how="left").dropna()
    Rest_locations['count'].max()

    basemap = generateBaseMap()
    HeatMap(Rest_locations[['lat','lon','count']].values.tolist(),zoom=20,radius=15).add_to(basemap)

    folium_static(basemap)


def generateBaseMap(default_location=[12.97, 77.59], default_zoom_start=12):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

