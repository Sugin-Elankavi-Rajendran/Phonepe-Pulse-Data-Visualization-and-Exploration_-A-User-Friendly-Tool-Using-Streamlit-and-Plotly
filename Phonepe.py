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

st.markdown(
    """
    <style>
    body {
        background-color: violet;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header(':white[Phonepe Pulse Data Visualization ]')