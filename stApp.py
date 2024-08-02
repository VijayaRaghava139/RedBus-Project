import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters

option = st.sidebar.radio('**Please Select Your Option**',['Home','Bus Info'])
if option == 'Home':
    def add_bg_from_local():
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://media.istockphoto.com/id/1161674685/photo/two-white-buses-traveling-on-the-asphalt-road-in-rural-landscape-at-sunset-with-dramatic.jpg?s=612x612&w=0&k=20&c=MnfC-FRX8q7yH-LHwX4jF4zOWpIm11Zyxgz2jLLDZwM=");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )

    add_bg_from_local()
    st.title('About Us')
    st.markdown('''
    **_We :blue-background[aim to revolutionize the transportation industry] by providing a comprehensive solution
    for collecting, analyzing and visualizing bus travel data. By utilizing Selenium for web scraping,
    we extract the detailed information from different sources including bus routes, schedules, prices, and seat availability.
    By streamlining data collection and providing powerful tools for data-driven decision-making,
    we :blue-background[improve operational efficiency and strategic planning in the transportation industry.]_**
    ''')
if option == 'Bus Info':
    def add_bg_from_local():
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://thumbs.dreamstime.com/z/concept-bus-route-map-d-rendering-207755719.jpg");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )

    add_bg_from_local()
    st.title('Bus Information Dashboard')
    df = pd.read_excel('busdata.xlsx')
    df = df[['Bus_Route_Name','Bus_Name','Bus_Type','Price','Star_Rating','Seat_Availability']]
    df = df.ffill()

    bus_filter = DynamicFilters(df=df, filters=['Bus_Route_Name','Bus_Name','Bus_Type','Price','Star_Rating'])
    bus_filter.display_filters(location='sidebar')
    bus_filter.display_df()
