#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install openpyxl
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit

import pickle
from pathlib import Path

import altair as alt

import streamlit_authenticator as stauth

#Streamlit run Ventas.py

st.set_page_config(page_title = 'Analisis Bolsa Australiana', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = 'moneybag:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

# ---- USER AUTHENTICATION ----

names = ["Camilo Diaz" , "Juliana Mesa"]
usernames = ["cjdiaz" , "jmesa"]
passwords = ["abc123" , "abc234"]

#load hashed passwords

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
authenticator = stauth.Authenticate( names, usernames, hashed_passwords, 'Analisis Bolsa Australiana', "abcdef", cookie_expiry_days = 30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    
if authentication_status == None:
    st.warning("Please enter your username and password")
    
if authentication_status:    


    st.title(':clipboard: Análisis de la Bolsa de Valores Australiana') #Titulo del Dash
    st.subheader('Realizado por: Camilo Diaz')
    st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown
    
    archivo_excel = 'Portafolio Australia.xlsx' 
    hoja_excel = 'Sheet1' 

    df = pd.read_excel(archivo_excel,
                       sheet_name = hoja_excel,
                       usecols = 'A:I')
                       #header = 0
        
    #st.dataframe(df) 
    
    #SIDEBAR
    
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f" Welcome {name}")    
    
    st.sidebar.header("Activos a filtrar:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
    Activo = st.sidebar.multiselect(
        "Seleccione el Activo:",
        options = df['Asset'].unique(),
        default = df['Asset'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
    )
    
    df_seleccion = df.query("Asset == @Activo " ) #el primero es la columna y el segundo es el selector

    st.dataframe(df_seleccion)
    
    line = alt.Chart(df_seleccion).mark_line().encode(
        alt.X("Date",title = "Date"),
        alt.Y("Close", title = "Closing Price",scale=alt.Scale(zero=False)),
        color = 'Asset'
    )
    line
                     
                     
                     
                     
