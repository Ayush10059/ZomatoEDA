import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Zomato Dashboard",
    page_icon = ":bar_chart:",
    layout="wide",
)

st.title("Zomato Data Visualization")

option_menu(
    menu_title=None,
    options=["Charts", "Maps" ],
    icons=["bar-chart-steps", "map"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

@st.cache
def get_data():
    df = pd.read_csv("data/zomato.csv")
    return df

df = get_data()

st.sidebar.header("Please Filter Here:")

listed_in_city = st.sidebar.multiselect(
    "Select City:",
    options=df["listed_in(city)"].unique(),
    default=df["listed_in(city)"].unique(),
)

listed_in_type = st.sidebar.multiselect(
    "Select Restaurant Type:",
    options=df["listed_in(type)"].unique(),
    default=df["listed_in(type)"].unique(),
)

df_selection = df.query(
    "`listed_in(city)` == @listed_in_city & `listed_in(type)` == @listed_in_type"
)

df_selection['approx_cost(for two people)'] = df_selection['approx_cost(for two people)'].replace(',', '', regex=True).dropna().astype(int)
df_selection['rate'] = df_selection['rate'].replace('NEW', None).replace('-', None).dropna().str[0:3].astype(float)

average_vote = int(df_selection['votes'].mean())
average_cost = int(df_selection['approx_cost(for two people)'].mean())
average_rating = round(df_selection['rate'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))

subheader_left_column, subheader_middle_column, subheader_right_column = st.columns(3)

with subheader_left_column:
    st.subheader("Average number of votes:")
    st.subheader(average_vote)

with subheader_middle_column:
    st.subheader("Approximate Average Cost For Two People:")
    st.subheader(average_cost)

with subheader_right_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

st.markdown("---")


body1_left_column, body1_right_column = st.columns(2)

with body1_left_column:
    st.header("Most famous restaurants chains")

    outletSlider = st.slider('Number of Outlets', min_value=5, max_value=10)

    outletFig = plt.figure(figsize=(5,3))
    outlets = df_selection['name'].value_counts()[:outletSlider]
    sns.barplot(x=outlets, y=outlets.index, palette='deep')
    st.pyplot(outletFig)

with body1_right_column:
    st.header("Most Popular Cuisines")

    cuisineSlider = st.slider('Number of Cuisines', min_value=5, max_value=10)

    cuisineFig = plt.figure(figsize=(5,3))
    cuisines = df_selection['cuisines'].value_counts()[:cuisineSlider]
    sns.barplot(x=cuisines, y=cuisines.index, palette='deep')
    st.pyplot(cuisineFig)

st.markdown("---")


body2_left_column, body2_right_column = st.columns(2)

with body2_left_column:
    st.header("Restaurant Types")

    typeSlider = st.slider('Number of Types', min_value=5, max_value=10)

    typeFig = plt.figure(figsize=(5,3))
    type = df_selection['rest_type'].value_counts()[:typeSlider]
    sns.barplot(x=type, y=type.index, palette='deep')
    st.pyplot(typeFig)

with body2_right_column:
    st.header("Popular locations")

    locationSlider = st.slider('Number of Locations', min_value=5, max_value=10)

    locationFig = plt.figure(figsize=(5,3))
    location=df_selection['location'].value_counts()[:locationSlider]
    sns.barplot(x=location, y=location.index, palette='deep')
    st.pyplot(locationFig)

st.markdown("---")


body3_left_column, body3_right_column = st.columns(2)

with body3_left_column:
    st.header("Can Order Online")

    online_order=df_selection['online_order'].value_counts()
    colors = ['#FEBFB3', '#E1396C']

    online_orderFig, ax1 = plt.subplots()
    ax1.pie(online_order, labels=online_order.index, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    st.pyplot(online_orderFig)

with body3_right_column:
    st.header("Can Book Table")

    book_table=df_selection['book_table'].value_counts()
    colors = ['#96D38C', '#D0F9B1']

    book_tableFig, ax1 = plt.subplots()
    ax1.pie(book_table, labels=book_table.index, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    st.pyplot(book_tableFig)

st.markdown("---")


body4_left_column, body4_right_column = st.columns(2)

with body4_left_column:
    st.header("Cost Distribution")

    cost_dist=df_selection[['rate','approx_cost(for two people)','online_order']].dropna()

    approx_costFig = plt.figure(figsize=(8,8))
    sns.histplot(cost_dist['approx_cost(for two people)'], kde=True)
    st.pyplot(approx_costFig)

with body4_right_column:
    st.header("Rating Distribution")

    ratingFig = plt.figure(figsize=(8,8))
    rating=df_selection['rate']
    sns.histplot(rating,bins=20, kde=True)
    st.pyplot(ratingFig)

st.markdown("---")


st.header("Cost VS Rating")

cost_distFig = plt.figure(figsize=(8,4))

sns.scatterplot(x="rate",y='approx_cost(for two people)',hue='online_order',data=cost_dist)
st.pyplot(cost_distFig)

st.markdown("---")


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            #header {visibility: hidden;}
            #footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
