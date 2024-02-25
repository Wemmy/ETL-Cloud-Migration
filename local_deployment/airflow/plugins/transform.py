# convert json to csv
import json, os, csv
import pandas as pd
from datetime import datetime, timedelta
from utils import *

current_date = datetime.now()
yesterday_date = current_date - timedelta(days=1)
yesterday_date_formated = yesterday_date.strftime('%Y-%m-%d')
month = current_date.strftime('%Y-%m')


# basic metrics
folder_names = ['balance_sheet_statement',
                'cashflow_statement',
                'income_statement',
                'key_metrics'
                ]

indicators = [
        'gdp.json',
        'gdp_per_capita.json',
        'treasury_yield.json',
        'fed_fund_rate.json',
        'cpi.json',
        'inflation.json',
        'retail_sales.json',
        'durables.json',
        'unemployment.json',
        'nonfarm_payroll.json'
    ]

def daily_transformation():
    # eod
    raw_root_path_eod = os.path.join('/opt/airflow/data', 'raw', month, get_key(current_date), 'eod')
    new_root_path_eod = os.path.join('/opt/airflow/data', 'transformed', month, get_key(current_date))
    # create data folder
    if not os.path.exists(new_root_path_eod):
        os.makedirs(new_root_path_eod)
    all_dfs = []
    # Iterate over all files in the folder
    for entry in os.listdir(raw_root_path_eod):
        full_path = os.path.join(raw_root_path_eod, entry)
        # Convert JSON to CSV
        with open(full_path, 'r') as j:
            data = json.load(j)
        df = pd.DataFrame(data['historical'])
        df['symbol'] = data['symbol']
    all_dfs.append(df)
    # Concatenate all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df.to_csv(os.path.join(new_root_path_eod, 'eod.csv'), index=False)

def monthly_transformation():
    raw_root_path = os.path.join('/opt/airflow/data', 'raw')
    new_root_path = os.path.join('/opt/airflow/data', 'transformed')
    folder_names = [os.path.join(raw_root_path, f) for f in folder_names]

    # transform tabular data
    for subdir, _, files in os.walk(raw_root_path):
        if subdir in folder_names:
            # file path
            csv_path = os.path.join(new_root_path, 
                                    os.path.relpath(subdir, raw_root_path), 
                                    os.path.relpath(subdir, raw_root_path)+'.csv'
                                    )
            all_dfs = []
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(subdir, file)

                    # Convert JSON to CSV
                    with open(json_path, 'r') as j:
                        data = json.load(j)
                    df = pd.DataFrame(data)
                    all_dfs.append(df)
            # Concatenate all dataframes
            combined_df = pd.concat(all_dfs, ignore_index=True)
            combined_df.to_csv(csv_path, index=False)

    path_json = os.path.join('data', 'raw', 'indicator')
    path_csv = os.path.join( 'data', 'transformed', 'indicator')
    # create data folder
    if not os.path.exists(path_csv):
        os.makedirs(path_csv)
    for f in indicators:
        json_to_csv(path_json, path_csv, f)



    


