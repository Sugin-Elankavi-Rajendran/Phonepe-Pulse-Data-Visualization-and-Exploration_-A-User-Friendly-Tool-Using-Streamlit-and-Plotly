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

