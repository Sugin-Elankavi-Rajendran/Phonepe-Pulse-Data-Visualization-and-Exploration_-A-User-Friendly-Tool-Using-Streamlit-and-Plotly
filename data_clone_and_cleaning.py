import git
import pandas as pd
import os
import json
from path import aggregated_transaction_path
from path import aggregated_user_path
from path import map_transaction_path
from path import map_user_path
from path import top_transaction_path


#url = "https://github.com/PhonePe/pulse.git"

#folder = "Phonepe"

#git.Repo.clone_from(url,folder)

##################

file1 = aggregated_transaction_path
aggregated_state_list = os.listdir(file1)

aggregated_transaction = {
    'State': [],
    'Year': [],
    'Quarter': [],
    'Transaction_type': [], 
    'Transaction_count': [], 
    'Transaction_amount': []
}

for aggregated_state_year in aggregated_state_list:
    a1 = os.path.join(file1,aggregated_state_year)
    aggregated_year_list = os.listdir(a1)

    for aggregated_state_year_data in aggregated_year_list:
        a2 = os.path.join(a1,aggregated_state_year_data)
        aggregated_year_list_data = os.listdir(a2)
        
        for aggregated_state_year_data_file in aggregated_year_list_data:
            a3 = os.path.join(a2,aggregated_state_year_data_file)
            data = open(a3,"r")
            files1 = json.load(data)

            for details in files1 ["data"]["transactionData"]:
                Name = details["name"]
                count = details ["paymentInstruments"][0]["count"]
                amount = details ["paymentInstruments"][0]["amount"]
                aggregated_transaction["State"].append(aggregated_state_year)
                aggregated_transaction["Year"].append(aggregated_state_year_data)
                aggregated_transaction["Quarter"].append(int(aggregated_state_year_data_file.strip(".json")))
                aggregated_transaction["Transaction_type"].append(Name)
                aggregated_transaction["Transaction_count"].append(count)
                aggregated_transaction["Transaction_amount"].append(amount)

df_aggregated_transactions = pd.DataFrame(aggregated_transaction)

####################

file2 = aggregated_user_path
aggregated_user_state_list = os.listdir(file2)

aggregated_user = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'Brands': [], 
    'User_Count': [], 
    'User_Percentage': []
}

for aggregated_state_year in aggregated_user_state_list:
    a1 = os.path.join(file2,aggregated_state_year)
    aggregated_year_list = os.listdir(a1)

    for aggregated_state_year_data in aggregated_year_list:
        a2 = os.path.join(a1,aggregated_state_year_data)
        aggregated_year_list_data = os.listdir(a2)
        
        for aggregated_state_year_data_file in aggregated_year_list_data:
            a3 = os.path.join(a2,aggregated_state_year_data_file)
            data = open(a3,"r")
            files2 = json.load(data)

            try:
                for details in files2 ["data"]["usersByDevice"]:
                    brand_name = details["brand"]
                    count_u = details ["count"]
                    percentage = details ["percentage"]
                    aggregated_user["State"].append(aggregated_state_year)
                    aggregated_user["Year"].append(aggregated_state_year_data)
                    aggregated_user["Quarter"].append(int(aggregated_state_year_data_file.strip(".json")))
                    aggregated_user["Brands"].append(brand_name)
                    aggregated_user["User_Count"].append(count_u)
                    aggregated_user["User_Percentage"].append(percentage)
            except:
                pass

df_aggregated_users = pd.DataFrame(aggregated_user)

##############

file3 = map_transaction_path
map_transaction_state_list = os.listdir(file3)

map_transaction = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'District': [], 
    'Transaction_Count': [], 
    'Transaction_Amount': []
}

for map_state in map_transaction_state_list:
    a1 = os.path.join(file3,map_state)
    map_year_list = os.listdir(a1)

    for map_state_year_data in map_year_list:
        a2 = os.path.join(a1,map_state_year_data)
        map_year_list_data = os.listdir(a2)
        
        for map_state_year_data_file in map_year_list_data:
            a3 = os.path.join(a2,map_state_year_data_file)
            data = open(a3,"r")
            files3 = json.load(data)

            for details in files3 ["data"]["hoverDataList"]:
                district_name = details["name"]
                mt_count = details ["metric"][0]["count"]
                mt_amount = details ["metric"][0]["amount"]
                map_transaction["State"].append(map_state)
                map_transaction["Year"].append(map_state_year_data)
                map_transaction["Quarter"].append(int(map_state_year_data_file.strip(".json")))
                map_transaction["District"].append(district_name)
                map_transaction["Transaction_Count"].append(mt_count)
                map_transaction["Transaction_Amount"].append(mt_amount)

df_map_transactions = pd.DataFrame(map_transaction)

##############

file4 = map_user_path
map_user_state_list = os.listdir(file4)

map_user = {
    "State": [], 
    "Year": [], 
    "Quarter": [], 
    "District": [], 
    "Registered_User": []
}

for map_state in map_user_state_list:
    a1 = os.path.join(file4,map_state)
    map_year_list = os.listdir(a1)

    for map_state_year_data in map_year_list:
        a2 = os.path.join(a1,map_state_year_data)
        map_year_list_data = os.listdir(a2)
        
        for map_state_year_data_file in map_year_list_data:
            a3 = os.path.join(a2,map_state_year_data_file)
            data = open(a3,"r")
            files4 = json.load(data)

            for details in files4["data"]["hoverData"].items():
                district = details[0]
                registered_user = details[1]["registeredUsers"]
                map_user["State"].append(map_state)
                map_user["Year"].append(map_state_year_data)
                map_user["Quarter"].append(int(map_state_year_data_file.strip(".json")))
                map_user["District"].append(district)
                map_user["Registered_User"].append(registered_user)

df_map_users = pd.DataFrame(map_user)

###############

file5 = top_transaction_path
top_transaction_state_list = os.listdir(file5)

top_transaction = {
    'State': [], 
    'Year': [], 
    'Quarter': [], 
    'District_Pincode': [], 
    'Transaction_count': [], 
    'Transaction_amount': []
}

for top_state in top_transaction_state_list:
    a1 = os.path.join(file5,top_state)
    top_year_list = os.listdir(a1)

    for top_state_year_data in top_year_list:
        a2 = os.path.join(a1,top_state_year_data)
        top_year_list_data = os.listdir(a2)
        
        for top_state_year_data_file in top_year_list_data:
            a3 = os.path.join(a2,top_state_year_data_file)
            data = open(a3,"r")
            files5 = json.load(data)

            for details in files5["data"]["pincodes"]:
                entity_name = details["entityName"]
                top_count = details["metric"]["count"]
                top_amount = details["metric"]["amount"]
                top_transaction["State"].append(top_state)
                top_transaction["Year"].append(top_state_year_data)
                top_transaction["Quarter"].append(int(top_state_year_data_file.strip(".json")))
                top_transaction["District_Pincode"].append(entity_name)
                top_transaction['Transaction_count'].append(top_count)
                top_transaction['Transaction_amount'].append(top_amount)

df_top_transactions = pd.DataFrame(top_transaction)

###############
