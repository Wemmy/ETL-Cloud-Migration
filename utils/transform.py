# convert json to csv
import json, os
import pandas as pd
from utils.alpha.transform import transform_indicator

# basic metrics
folder_names = ['balance_sheet_statement',
                'cashflow_statement',
                'eod',
                'income_statement',
                'key_metrics'
                ]

raw_root_path = os.path.join('data', 'raw')
# create mother folder
new_root_path = os.path.join('data', 'transformed')

folder_names = [os.path.join(raw_root_path, f) for f in folder_names]

def transform():
    # transform tabular data
    for subdir, _, files in os.walk(raw_root_path):
        if subdir in folder_names:
            # file path
            csv_path = os.path.join(new_root_path, 
                                    os.path.relpath(subdir, raw_root_path), 
                                    os.path.relpath(subdir, raw_root_path)+'.csv'
                                    )
            # Create subdirectory in transformed folder if it doesn't exist
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)

            all_dfs = []

            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(subdir, file)

                    # Convert JSON to CSV
                    with open(json_path, 'r') as j:
                        data = json.load(j)
                    if subdir.endswith('eod'):
                        df = pd.DataFrame(data['historical'])
                        df['symbol'] = data['symbol']
                    else:
                        df = pd.DataFrame(data)
                    all_dfs.append(df)

            # Concatenate all dataframes
            combined_df = pd.concat(all_dfs, ignore_index=True)
            combined_df.to_csv(csv_path, index=False)

    transform_indicator()

    
if not os.path.exists(new_root_path):
    transform()


