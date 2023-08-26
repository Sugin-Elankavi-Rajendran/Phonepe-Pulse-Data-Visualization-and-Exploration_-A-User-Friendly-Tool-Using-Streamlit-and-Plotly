import streamlit as st
import mysql
import mysql.connector
import pandas as pd
import numpy as np
import json
import requests
import subprocess
from path import geo_data
import plotly
import plotly.express as px
from path import logo_path

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
st.markdown(
    f"""
    <style>
        .logo-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }}
        .logo-img {{
            max-width: 200px;
            height: auto;
        }}
    </style>
    <div class="logo-container">
        <img src="{logo_path}" alt="Logo" class="logo-img">
    </div>
    """,
    unsafe_allow_html=True
)
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

    cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transactions WHERE Year = '{selected_year}' AND Quarter = '{selected_Quarter}' AND Transaction_type = '{transaction_type}';")
    count_query_result = cursor.fetchall()
    df_count_query_result = pd.DataFrame(np.array(count_query_result), columns=['Total','Average'])
    modified_df_count_query_result = df_count_query_result.set_index(['Average'])

    df_query_result.drop(columns=['State'], inplace=True)
    url = geo_data
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_transaction = [feature['properties']['ST_NM'] for feature in data1['features']]
    state_names_transaction.sort()
    df_state_names_transaction = pd.DataFrame({'State': state_names_transaction})
    df_state_names_transaction['Transaction_amount']=df_query_result
    df_state_names_transaction.to_csv('State_trans.csv', index=False)
    df_transaction = pd.read_csv('State_trans.csv')
    fig_tra = px.choropleth(
        df_transaction,
        geojson= geo_data,
        featureidkey='properties.ST_NM',
        locations='State',
        color='Transaction_amount',
        color_continuous_scale='thermal',
        title = 'Transaction Analysis'
    )
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(title_font=dict(size=33),title_font_color='#fdfcff', height=800)
    st.plotly_chart(fig_tra,use_container_width=True)

    modified_df_query_result['State'] = modified_df_query_result['State'].astype(str)
    modified_df_query_result['Transaction_amount'] = modified_df_query_result['Transaction_amount'].astype(float)
    modified_df_query_result_fig = px.bar(modified_df_query_result , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 700,)
    modified_df_query_result_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
    st.plotly_chart(modified_df_query_result_fig,use_container_width=True)

    st.header('Total calculation')

    col4, col5 = st.columns(2)
    with col4:
        st.subheader('Transaction Analysis')
        st.dataframe(modified_df_table_query_result)
    with col5:
        st.subheader('Transaction Amount')
        st.dataframe(modified_df_amount_query_result)
        st.subheader('Transaction Count')
        st.dataframe(modified_df_count_query_result)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            in_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_us_yr')
        with col2:
            in_us_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_us_qtr')
        
        cursor.execute(f"SELECT State, SUM(User_Count) FROM aggregated_users WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY State;")
        in_us_tab_qry_rslt = cursor.fetchall()
        df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['State', 'User Count'])
        df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt)+1)))

        cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_users WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
        in_us_co_qry_rslt = cursor.fetchall()
        df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total','Average'])
        df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])

        df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
        url = geo_data
        response = requests.get(url)
        data2 = json.loads(response.content)
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        df_state_names_use['User Count']=df_in_us_tab_qry_rslt
        df_state_names_use.to_csv('State_user.csv', index=False)
        df_use = pd.read_csv('State_user.csv')
        fig_use = px.choropleth(
            df_use,
            geojson=geo_data,
            featureidkey='properties.ST_NM',
            locations='State',
            color='User Count',
            color_continuous_scale='thermal',
            title = 'User Analysis'
        )
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33),title_font_color='#fdfcff', height=800)
        st.plotly_chart(fig_use,use_container_width=True)

        df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
        df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
        df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1 , x = 'State', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 700,)
        df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
        st.plotly_chart(df_in_us_tab_qry_rslt1_fig,use_container_width=True)

        st.header('Total calculation')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_in_us_tab_qry_rslt1)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_in_us_co_qry_rslt1)

elif option =='State wise':

    tab3, tab4 = st.tabs(['Transaction','User'])

    with tab3:

        col1, col2,col3 = st.columns(3)
        with col1:
            st_tr_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_tr_st')
        with col2:
            st_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_tr_yr')
        with col3:
            st_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='st_tr_qtr')
        
        cursor.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transactions WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_tr_tab_bar_qry_rslt = cursor.fetchall()
        df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt), columns=['Transaction_type', 'Transaction_amount'])
        df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt)+1)))

        cursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transactions WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_tr_anly_tab_qry_rslt = cursor.fetchall()
        df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt), columns=['Transaction_type','Transaction_count','Transaction_amount'])
        df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt)+1)))

        cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transactions WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_tr_am_qry_rslt = cursor.fetchall()
        df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Total','Average'])
        df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])
        
        cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transactions WHERE State = '{st_tr_st}' AND Year ='{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_tr_co_qry_rslt = cursor.fetchall()
        df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Total','Average'])
        df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])

        df_st_tr_tab_bar_qry_rslt1['Transaction_type'] = df_st_tr_tab_bar_qry_rslt1['Transaction_type'].astype(str)
        df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(float)
        df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1 , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 500,)
        df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
        st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig,use_container_width=True)

        st.header('Total calculation')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Analysis')
            st.dataframe(df_st_tr_anly_tab_qry_rslt1)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_st_tr_am_qry_rslt1)
            st.subheader('Transaction Count')
            st.dataframe(df_st_tr_co_qry_rslt1)

    with tab4:
        
        col5, col6 = st.columns(2)
        with col5:
            st_us_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_us_st')
        with col6:
            st_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_us_yr')
        
        cursor.execute(f"SELECT Quarter, SUM(User_Count) FROM aggregated_users WHERE State = '{st_us_st}' AND Year = '{st_us_yr}' GROUP BY Quarter;")
        st_us_tab_qry_rslt = cursor.fetchall()
        df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['Quarter', 'User Count'])
        df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt)+1)))

        cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_users WHERE State = '{st_us_st}' AND Year = '{st_us_yr}';")
        st_us_co_qry_rslt = cursor.fetchall()
        df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['Total','Average'])
        df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['Average'])

        df_st_us_tab_qry_rslt1['Quarter'] = df_st_us_tab_qry_rslt1['Quarter'].astype(int)
        df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
        df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1 , x = 'Quarter', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 500,)
        df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
        st.plotly_chart(df_st_us_tab_qry_rslt1_fig,use_container_width=True)

        st.header('Total calculation')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('User Analysis')
            st.dataframe(df_st_us_tab_qry_rslt1)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_st_us_co_qry_rslt1)

else:

    tab5, tab6 = st.tabs(['Transaction','User'])

    with tab5:
        top_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_tr_yr')

        cursor.execute(f"SELECT State, SUM(Transaction_amount) As Transaction_amount FROM top_transactions WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_tr_tab_qry_rslt = cursor.fetchall()
        df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt), columns=['State', 'Top Transaction amount'])
        df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_tab_qry_rslt)+1)))

        cursor.execute(f"SELECT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transactions WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_tr_anly_tab_qry_rslt = cursor.fetchall()
        df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt), columns=['State', 'Top Transaction amount','Total Transaction count'])
        df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt)+1)))

        df_top_tr_tab_qry_rslt1['State'] = df_top_tr_tab_qry_rslt1['State'].astype(str)
        df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1['Top Transaction amount'].astype(float)
        df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1 , x = 'State', y ='Top Transaction amount', color ='Top Transaction amount', color_continuous_scale = 'thermal', title = 'Top Transaction Analysis Chart', height = 600,)
        df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
        st.plotly_chart(df_top_tr_tab_qry_rslt1_fig,use_container_width=True)

        st.header('Total calculation')
        st.subheader('Top Transaction Analysis')
        st.dataframe(df_top_tr_anly_tab_qry_rslt1)

    with tab6:
        top_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_us_yr')

        cursor.execute(f"SELECT State, SUM(Registered_User) AS Top_users FROM top_users WHERE Year='{top_us_yr}' GROUP BY State ORDER BY Top_users DESC LIMIT 10;")
        top_us_tab_qry_rslt = cursor.fetchall()
        df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['State', 'Total User count'])
        df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_us_tab_qry_rslt)+1)))

        df_top_us_tab_qry_rslt1['State'] = df_top_us_tab_qry_rslt1['State'].astype(str)
        df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
        df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1 , x = 'State', y ='Total User count', color ='Total User count', color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 600,)
        df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#fdfcff')
        st.plotly_chart(df_top_us_tab_qry_rslt1_fig,use_container_width=True)

        st.header('Total calculation')
        st.subheader('Total User Analysis')
        st.dataframe(df_top_us_tab_qry_rslt1)