import streamlit as st
import mysql
import mysql.connector

################

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database = "phonepe"
)
    
cursor = connection.cursor()

#####################

st.set_page_config(layout='wide')
st.header('Phonepe Data')
st.write("The following data is from the year 2018-2022:")

##################

option = st.radio("**Select anyone of the following option:**",('All of India', 'State wise','Top Ten categories'),horizontal=True)

##################

if option == 'All of India':
     tab1, tab2 = st.tabs(['Transactions','Users'])
     
     with tab1:
        column1, column2, column3 = st.columns(3)
        with column1:
            selected_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'))
        with column2:
            selected_Quarter = st.selectbox('**Select Quarter**', ('1st Quarter','2nd Quarter','3rd Quarter','4th Quarter'),key='selected_Quarter')
        with column3:
            top_ten_categories = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='top_ten_categories')
        