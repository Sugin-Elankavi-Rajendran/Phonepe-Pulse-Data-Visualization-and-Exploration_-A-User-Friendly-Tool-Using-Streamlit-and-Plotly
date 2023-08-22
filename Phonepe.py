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

option = st.radio("Select anyone of the following option:",('All India', 'State wise','Top Ten categories'),horizontal=True)

##################