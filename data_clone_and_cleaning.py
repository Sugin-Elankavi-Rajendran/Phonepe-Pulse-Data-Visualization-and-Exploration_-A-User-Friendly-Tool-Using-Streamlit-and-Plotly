import git
import pandas as pd
import os
import json
from path import aggregated_path

#url = "https://github.com/PhonePe/pulse.git"

#folder = "Phonepe"

#git.Repo.clone_from(url,folder)

##################

file1 = aggregated_path
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
            file = json.load(data)

            for details in file ["data"]["transactionData"]:
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

