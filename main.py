import streamlit as st

from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Zomato Dashboard",
    page_icon = ":bar_chart:",
    layout="wide",
)

from charts import charts_page
from maps import map_page

st.title("Zomato Data Visualization")

selected_page = option_menu(
    menu_title=None,
    options=["Charts", "Maps" ],
    icons=["bar-chart-steps", "map"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected_page == "Charts":
    charts_page()
    
elif selected_page == "Maps":
    map_page()

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                #header {visibility: hidden;}
                #footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)
