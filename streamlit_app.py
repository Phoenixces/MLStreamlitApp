import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import time  # to simulate a real time data, time loop
import requests
import pandas as pd
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from streamlit_card import card
from random import randint

#Loading the saved models
classif_model = pickle.load(open('potability_model.sav', 'rb'))

st.set_page_config(
    page_icon="💧",
    layout="wide",
    page_title="Dashboard-ML"
    )

#Creating the sidebar for navigation
with st.sidebar:
    selected = option_menu('Smart Environmental Analysis',
                            ['Real Time Environmental Data For Bangalore', 'Water Quality Classification'],
                            icons= ['speedometer','moisture'],
                            default_index=0)
    
url1 = "https://sheets.googleapis.com/v4/spreadsheets/1f7B3W414lMUss8IRqg4MxGDQtPfDIpKhOfIroDOF4L0/values/water_potability?alt=json&key=AIzaSyBkNIPq-k727y-Z-Pndctoeg-bkPnDi9Fg ";
data = requests.get(url1).json()
valLen = len(data['values'])

dataset = [data['values'][i]  for i in range(1, valLen, 1)]
df = pd.DataFrame(dataset, columns= ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Potability'])

df ['ph'] = pd.to_numeric(df['ph'], errors='coerce')
df ['Hardness'] = pd.to_numeric(df['Hardness'], errors='coerce')
df ['Solids'] = pd.to_numeric(df['Solids'], errors='coerce')
df ['Chloramines'] = pd.to_numeric(df['Chloramines'], errors='coerce')
df ['Sulfate'] = pd.to_numeric(df['Sulfate'], errors='coerce')
df ['Conductivity'] = pd.to_numeric(df['Conductivity'], errors='coerce')
df ['Organic_carbon'] = pd.to_numeric(df['Organic_carbon'], errors='coerce')
df ['Trihalomethanes'] = pd.to_numeric(df['Trihalomethanes'], errors='coerce')
df ['Turbidity'] = pd.to_numeric(df['Turbidity'], errors='coerce')

#Data cleaning 
df = df.replace(np.nan, 0, regex=True)


# Sidepannel Operations  
placeholder  = st.empty()
with placeholder.container():
    
     #----------------------------------------------------------Dashboard Onwards-----------------------------------------------------------#
        
    if(selected == 'Real Time Environmental Data For Bangalore'):
        
        # ------Air----
        airResponse = requests.get("https://api.meersens.com/environment/public/air/current?lat=12.9716&lng=77.5946&index_type=meersens&health_recommendations=false&apikey=VakDwnFu895dDSNP3LaRz8goupR856se")
        dataAir = airResponse.json()
        valueAir = dataAir['index']['value']
        
        
        #-------UV-----
        uvResponse = requests.get("https://api.meersens.com/environment/public/uv/current?lat=12.9716&lng=77.5946&index_type=meersens&health_recommendations=false&apikey=VakDwnFu895dDSNP3LaRz8goupR856se")
        dataUV = uvResponse.json()
        valueUV = dataUV['index']['value']
        
        #------temp----
        tempResponse = requests.get("https://api.meersens.com/environment/public/weather/current?lat=12.9716&lng=77.5946&index_type=meersens&health_recommendations=false&apikey=VakDwnFu895dDSNP3LaRz8goupR856se")
        datatemp = tempResponse.json()
        valueTemp = datatemp['index']['value']
        
        #-----water----
        WQIResponse = requests.get("https://api.meersens.com/environment/public/water/current?lat=12.9716&lng=77.5946&index_type=meersens&health_recommendations=false&apikey=VakDwnFu895dDSNP3LaRz8goupR856se")
        datawater = WQIResponse.json()
        valueWater = datawater['index']['value']
        
        st.header("Green Gauge 💻 ")
        col1, col2 = st.columns([12, 1])
        st.divider()
        
        with col1:
            st.markdown("#### Current Values")
            st.divider()
            st.text("")
            col1, col2, col3, col4 = st.columns([3, 3, 3, 3], gap="large")
            with col1:
                st.metric("AQI", value = valueAir)
                st.write(dataAir['index']['description'])
            with col2:   
                st.metric("UV", value = valueUV)
                st.write(dataUV['index']['description'])
            with col3:
                st.metric("Temperature", value = valueTemp)
                st.write(datatemp['index']['description'])
            with col4:
                st.metric("WQI", value = valueWater)
                st.write(datawater['index']['description'])
            
            st.divider()
            st.text("")
            st.empty()
            st.markdown('#### Water Potability Dataset')
            st.dataframe(df, height = 800, width = 900)

    
    #----------------------------------------------------------Classification Onwards-----------------------------------------------------------#    
        
    #water Quality Classification
    if(selected == 'Water Quality Classification'):

        col1, col2, col3 = st.columns([1, 7, 1], gap="medium")
        
        #On user values
        with col2:
            wq = ''

            #Page Title
            st.subheader("Check Portability, For User Provided Values:")
            st.divider()

            #For blank line
            st.text("")
            st.empty()
            
            col1, col2, col3 = st.columns([1, 4, 1], gap="small");
            with col2:
                pH = st.text_input('ph: ', key = 50)
                hardness = st.text_input('Hardness: ', key = 60)
                solids = st.text_input('Solids: ', key = 70)
                Cholaramines = st.text_input('Chloramines: ', key = 80)
                Sulfate = st.text_input('Sulfate: ', key = 90)
                Conductivity = st.text_input('Conductivity: ', key = 100)
                Organic_carbon = st.text_input('Organic_carbon: ', key = 110)
                Trihalomethanes = st.text_input('Trihalomethanes: ', key = 120)
                Turbidity = st.text_input('Turbidity: ', key = 130)

                
                try:
                        #Creating a button for prediction
                        if st.button('Get Potability', 2):
                            potability = int(str(classif_model.predict([[float(pH), float(hardness), float(solids), float(Cholaramines), float(Sulfate), float(Conductivity), float(Organic_carbon), float(Trihalomethanes), float(Turbidity)]])).replace(']', '').replace('[', ''))
                            if(potability):
                                wq = "Water is Potable :)"
                            else:
                                wq = "Water is Not Potable :("
                        st.success(wq)
            
                except ValueError as ve:
                        st.success("Invalid Input")


