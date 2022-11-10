import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Zomato Dashboard",
    page_icon = ":bar_chart:",
    layout="wide",
)


st.title("Main Page")

# if "my_input" not in st.session_state:
    # st.session_state[]

df = pd.read_csv("data/zomato.csv")


head = df.head

print(df.columns)

st.sidebar.header("Please Filter Here:")
# st.sidebar.success("Select a page above.")

listed_in_city = st.sidebar.multiselect(
    "Select City:",
    options=df["listed_in(city)"].unique(),
    default="BTM",
)

listed_in_type = st.sidebar.multiselect(
    "Select Restaurant Type:",
    options=df["listed_in(type)"].unique(),
    default=df["listed_in(type)"].unique(),
)

df_selection = df.query(
    "`listed_in(city)` == @listed_in_city & `listed_in(type)` == @listed_in_type"
)


print(df_selection['votes'].unique())
print(df_selection['approx_cost(for two people)'].unique())
print(df_selection['rate'].unique())

df_selection['approx_cost(for two people)'] = df_selection['approx_cost(for two people)'].replace(',', '', regex=True).fillna('1000').astype(int)
df_selection['rate'] = df_selection['rate'].replace('NEW', '2.5').replace('-', '2.5').fillna('2.5').str[0:3].astype(float)

average_vote = int(df_selection['votes'].mean())
average_cost = int(df_selection['approx_cost(for two people)'].mean())
average_rating = round(df_selection['rate'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Average number of votes:")
    st.subheader(average_vote)

with middle_column:
    st.subheader("Approximate Average Cost For Two People:")
    st.subheader(average_cost)

with right_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

st.markdown("---")

st.write("Most famous restaurants chains")
outletSlider = st.slider('Number of Outlets', min_value =5, max_value=20)

outletFig = plt.figure(figsize=(7,7))
outlets = df_selection['name'].value_counts()[:outletSlider]
sns.barplot(x=outlets, y=outlets.index, palette='deep')
st.pyplot(outletFig)

st.markdown("---")

st.write("Restaurant Types")
typeSlider = st.slider('Number of Types', min_value=5, max_value=20)

typeFig = plt.figure(figsize=(7,7))
type = df_selection['rest_type'].value_counts()[:typeSlider]
sns.barplot(x=type, y=type.index)
st.pyplot(typeFig)

st.markdown("---")

plt.title("Most Popular Cuisines")
cuisineSlider = st.slider('Number of Cuisines', min_value=5, max_value=20)

cuisineFig = plt.figure(figsize=(7,7))
cuisines = df_selection['cuisines'].value_counts()[:cuisineSlider]
sns.barplot(x=cuisines, y=cuisines.index)
st.pyplot(cuisineFig)

st.markdown("---")
