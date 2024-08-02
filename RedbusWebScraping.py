import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#Creating Empty Lists for each column
bus_route_name=[]
bus_name=[]
bus_type=[]
departing_time=[]
duration=[]
reaching_time=[]
star_rating=[]
price=[]
seat_availability=[]

for i in range(1,26):
    
    #Initializing the Chrome Browser window and get the required Webpage
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://www.redbus.in/bus-tickets/routes-directory')

    #Clicking the route link and get the Busses Information
    route = driver.find_element('xpath','/html/body/div[1]/div/article/div[1]/ul/li[{0}]/a'.format(i)).text
    driver.find_element('xpath','/html/body/div[1]/div/article/div[1]/ul/li[{0}]/a'.format(i)).click()
    driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[1]/div/div/div[2]').click()
    driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[1]/section/div/div[3]/div/div[1]/div/input').click()
    driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[1]/section/div/div[3]/div/div[2]/div[3]/span[5]/div[2]/span').click()
    driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[1]/section/div/div[4]/button').click()
    time.sleep(3)

    #Scrolling the Webpage to the End
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        new_height=driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height=new_height

    #Extract the text out of each element and add them to respective empty lists declared
    total = driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[1]/div[1]/span[1]/span').text.split()[0]
    for i in range(1,int(total)+1):
        bus_route_name.append(route)
        try:
            bus_name.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[1]/div[1]'.format(i)).text)
        except:
            bus_name.append('NA')
        try:
            bus_type.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[1]/div[2]'.format(i)).text)
        except:
            bus_type.append('NA')
        try:
            departing_time.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[2]/div[1]'.format(i)).text)
        except:
            departing_time.append('NA')
        try:
            duration.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[3]/div'.format(i)).text)
        except:
            duration.append('NA')
        try:
            reaching_time.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[4]/div[1]'.format(i)).text)
        except:
            reaching_time.append('NA')
        try:
            star_rating.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[5]/div[1]/div/span'.format(i)).text)
        except:
            star_rating.append('NA')
        try:
            price.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[6]/div/div[2]/span'.format(i)).text)
        except:
            price.append('NA')
        try:
            seat_availability.append(driver.find_element('xpath','/html/body/section/div[2]/div[4]/div/div[2]/div/div[2]/div[2]/div/ul/div[{0}]/li/div/div[1]/div[1]/div[7]/div[1]'.format(i)).text.split()[0])
        except:
            seat_availability.append('NA')
    driver.quit()

#Declare a dictionary with each list as value,Column names as Keys and form a Pandas dataframe with the dictionary
total_records = {'Bus_Route_Name':bus_route_name,'Bus_Name':bus_name,'Bus_Type':bus_type,'Departing_Time':departing_time,'Duration':duration,'Reaching_Time':reaching_time,'Star_Rating':star_rating,'Price':price,'Seat_Availability':seat_availability}
df = pd.DataFrame(total_records)
print(df)

#Connect Python to MYSQL and Export the Pandas dataframe to MYSQL
mydb = mysql.connector.connect(host='localhost', user='root', password='root', database="redbus")
mycursor = mydb.cursor()
query = 'CREATE TABLE busdata (id INT AUTO_INCREMENT PRIMARY KEY,Bus_Route_Name VARCHAR(255),Bus_Name VARCHAR(255),Bus_Type VARCHAR(255),Departing_Time VARCHAR(255),Duration VARCHAR(255),Reaching_Time VARCHAR(255),Star_Rating VARCHAR(255),Price VARCHAR(255),Seat_Availability VARCHAR(255))'
mycursor.execute(query)
engine = create_engine('mysql+mysqlconnector://root:root@localhost/redbus')
df.to_sql('busdata', con=engine, if_exists='append', index=False)

driver.quit()
