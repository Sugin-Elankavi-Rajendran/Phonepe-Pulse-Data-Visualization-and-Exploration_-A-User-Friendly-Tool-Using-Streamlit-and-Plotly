import streamlit as st
import mysql
import mysql.connector
import pandas as pd
import numpy as np
import json
import requests
import subprocess

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
            selected_year = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='selected_year')
        with column2:
            selected_Quarter = st.selectbox('**Select Quarter**', ('1st Quarter','2nd Quarter','3rd Quarter','4th Quarter'),key='selected_Quarter')
        with column3:
            transaction_type = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='top_ten_categories')
               
        cursor.execute(f"SELECT State, Transaction_amount FROM aggregated_transactions WHERE Year = '{selected_year}' AND Quarter = '{selected_Quarter}' AND Transaction_type = '{transaction_type}';")
        query_result = cursor.fetchall()
        df_query_result = pd.DataFrame(np.array(query_result), columns=['State', 'Transaction_amount'])
        modified_df_query_result = df_query_result.set_index(pd.Index(range(1, len(df_query_result)+1)))

        cursor.execute(f"SELECT State, Transaction_count, Transaction_amount FROM aggregated_transactions WHERE Year = '{selected_year}' AND Quarter = '{selected_Quarter}' AND Transaction_type = '{transaction_type}';")
        table_query_result = cursor.fetchall()
        df_table_query_result = pd.DataFrame(np.array(table_query_result), columns=['State','Transaction_count','Transaction_amount'])
        modified_df_table_query_result = df_table_query_result.set_index(pd.Index(range(1, len(df_table_query_result)+1)))

        cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transactions WHERE Year = '{selected_year}' AND Quarter = '{selected_Quarter}' AND Transaction_type = '{transaction_type}';")
        amount_query_result = cursor.fetchall()
        df_amount_query_result = pd.DataFrame(np.array(amount_query_result), columns=['Total','Average'])
        modified_df_amount_query_result = df_amount_query_result.set_index(['Average'])
 
        cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Year = '{selected_year}' AND Quarter = '{selected_Quarter}' AND Transaction_type = '{transaction_type}';")
        count_query_result = cursor.fetchall()
        df_count_query_result = pd.DataFrame(np.array(count_query_result), columns=['Total','Average'])
        modified_df_count_query_result = df_count_query_result.set_index(['Average'])

        df_query_result.drop(columns=['State'], inplace=True)
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        # Create a DataFrame with the state names column
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        # Combine the Gio State name with df_in_tr_tab_qry_rslt
        df_state_names_tra['Transaction_amount']=df_in_tr_tab_qry_rslt
        # convert dataframe to csv file
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        # Read csv
        df_tra = pd.read_csv('State_trans.csv')
        # Geo plot
        fig_tra = px.choropleth(
            df_tra,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='thermal',title = 'Transaction Analysis')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_tra,use_container_width=True)

        # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
        df_in_tr_tab_qry_rslt1['State'] = df_in_tr_tab_qry_rslt1['State'].astype(str)
        df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
        df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1 , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 700,)
        df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_in_tr_tab_qry_rslt1_fig,use_container_width=True)

        # -------  /  All India Total Transaction calculation Table   /   ----  #
        st.header(':violet[Total calculation]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_in_tr_anly_tab_qry_rslt1)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_in_tr_am_qry_rslt1)
            st.subheader('Transaction Count')
            st.dataframe(df_in_tr_co_qry_rslt1)