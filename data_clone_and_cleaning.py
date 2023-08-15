import git
import pandas as pd
import os
import json
from path import aggregated_transaction_path
from path import aggregated_user_path

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