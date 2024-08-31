import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

db_conn = mysql.connector.connect (
                host = 'localhost',
                user = 'root',
                password = 'root',
                database = 'redbus'
               )
mycursor = db_conn.cursor()
# mycursor.execute('SELECT * FROM BUSINFO')
# data = mycursor.fetchall()

option = st.sidebar.radio('**Please Select Your Option**',['Home','Bus Info'], horizontal=True)

if option == 'Home':
    
    def add_bg_from_local():
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://as2.ftcdn.net/v2/jpg/05/79/39/81/1000_F_579398114_CSdxRI5fuLIxZWXXYenwcyjkErOLpM4z.jpg");
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
    st.sidebar.header('Filter Options')

    column_list = ['Bus_Route_Name','Bus_Name','Bus_Type','Star_Rating']
    column_filters = {}
    for column in column_list:
        mycursor.execute(f'select distinct {column} from businfo')
        values = [row[0] for row in mycursor.fetchall()]
        selected_values = st.sidebar.multiselect(f'Select {column}', values)
        column_filters[column] = selected_values
    price = st.sidebar.slider('Chose Price_Range',min_value=100,max_value=5000,value=1350,step=50)
    
    def fetch_filtered_data(column_filters):
        query = "SELECT * FROM businfo WHERE 1=1"
    
        # Dynamically build the WHERE clause based on filters
        for column, values in column_filters.items():
            if values:
                placeholders = ', '.join(['%s'] * len(values))
                query += f' AND {column} IN ({placeholders})'
        query += f' AND price < {price}'
        
        # Execute the query
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute(query, [value for sublist in column_filters.values() for value in sublist])
        data = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(data)

    if st.button('Apply Filters'):
        filtered_data = fetch_filtered_data(column_filters)
        st.write(filtered_data)




























    
    

    # mycursor.execute('select distinct Bus_Name from businfo')
    # bus_name = mycursor.fetchall()
    # bus_names = []
    # for name in bus_name:
    #     bus_names.append(str(name).split('\'')[1])

    # mycursor.execute('select distinct Bus_Type from businfo')
    # bus_type = mycursor.fetchall()
    # bus_types = []
    # for types in bus_type:
    #     bus_types.append(str(types).split('\'')[1])

    # Bus_Route_Name = st.sidebar.multiselect('Select Route', bus_route_names),
    # Bus_Name = st.sidebar.multiselect('Select Travels', bus_names),
    # Bus_Type = st.sidebar.multiselect('Select Bus Type', bus_types),
    # Star_Rating = st.sidebar.number_input('Rating Preference',min_value=0.0,max_value=5.0,value=4.3,step=0.1),
    # price = st.sidebar.slider('Chose Price Range',min_value=100,max_value=5000,value=1350,step=50)
    # sample = {}
    # sample['Bus_Name'] = Bus_Name
    # placeholders = ', '.join(['%s'] * len(values))
    # print(placeholders)

    # if len(Bus_Route_Name[0]) != 0:
    #     if len(Bus_Route_Name[0])==1:
    #         query = f'select * from businfo where Bus_Route_Name = "{Bus_Route_Name[0][0]}" and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     elif len(Bus_Route_Name[0])>1:
    #         routes = tuple(Bus_Route_Name[0])
    #         query = f'select * from businfo where Bus_Route_Name in {routes} and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     else:
    #         pass
    #         #query = f'select * from businfo where price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     df1 = pd.read_sql(query, db_conn)
    #     st.write(df1)
        
    # elif len(Bus_Name[0]) != 0:
    #     if len(Bus_Name[0])==1:
    #         query = f'select * from businfo where Bus_Name = "{Bus_Name[0][0]}" and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     elif len(Bus_Name[0])>1:
    #         routes = tuple(Bus_Name[0])
    #         query = f'select * from businfo where Bus_Name in {routes} and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     else:
    #         pass
    #         #query = f'select * from businfo where price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     df1 = pd.read_sql(query, db_conn)
    #     st.write(df1)
        
    # elif len(Bus_Type[0]) != 0:
    #     if len(Bus_Type[0])==1:
    #         query = f'select * from businfo where Bus_Type = "{Bus_Type[0][0]}" and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     elif len(Bus_Type[0])>1:
    #         routes = tuple(Bus_Type[0])
    #         query = f'select * from businfo where Bus_Type in {routes} and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     else:
    #         pass
    #         #query = f'select * from businfo where price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     df1 = pd.read_sql(query, db_conn)
    #     st.write(df1)
    
    # else:
    #     query = f'select * from businfo where price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     df1 = pd.read_sql(query, db_conn)
    #     st.write(df1)

    # if len(Bus_Route_Name[0]) != 0 and len(Bus_Name[0]) != 0 and len(Bus_Type[0]) != 0:
    #     if len(Bus_Route_Name[0])==1 and len(Bus_Name[0])==1 and len(Bus_Type[0])==1:
    #         query = f'select * from businfo where Bus_Route_Name = "{Bus_Route_Name[0][0]}" and Bus_Name = "{Bus_Name[0][0]}" and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     elif len(Bus_Route_Name[0])>1:
    #         routes = tuple(Bus_Route_Name[0])
    #         query = f'select * from businfo where Bus_Route_Name in {routes} and price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     else:
    #         pass
    #         #query = f'select * from businfo where price < {price} and Star_Rating = {float(Star_Rating[0])}'
    #     df1 = pd.read_sql(query, db_conn)
    #     st.write(df1)
    

    