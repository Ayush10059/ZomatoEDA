import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv("data/zomato.csv")

st.write("Most famous restaurants chains in Bangaluru")
outletSlider = st.slider('Number of outlets', min_value =5, max_value=20)

outletFig = plt.figure(figsize=(7,7))
outlets = df['name'].value_counts()[:outletSlider]
sns.barplot(x=outlets,y=outlets.index,palette='deep')
st.pyplot(outletFig)


st.write("Restaurant types")
typeSlider = st.slider('Number of types', min_value=5, max_value=20)

typeFig = plt.figure(figsize=(7,7))
type = df['rest_type'].value_counts()[:typeSlider]
sns.barplot(x=type,y=type.index)
st.pyplot(typeFig)


plt.title("Most popular cuisines of Bangalore")
cuisineSlider = st.slider('Number of cuisines', min_value=5, max_value=20)

cuisineFig = plt.figure(figsize=(7,7))
cuisines = df['cuisines'].value_counts()[:cuisineSlider]
sns.barplot(x=cuisines,y=cuisines.index)
st.pyplot(cuisineFig)


ratingFig = plt.figure(figsize=(6,5))
rating = df['rate'].dropna().apply(lambda x : float(x.split('/')[0]) if (len(x)>3)  else np.nan ).dropna()
sns.distplot(rating,bins=20)
st.pyplot(ratingFig)
