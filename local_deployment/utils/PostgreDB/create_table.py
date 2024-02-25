from db_connect import *
import os 
import csv


folder_path_pg = os.path.join('data', 'transformed')

conn = create_connection(DB_ENDPOINT, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME)
cur = conn.cursor()

for subdir, _, files in os.walk(folder_path_pg):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(subdir, file)
            table_name = os.path.splitext(file)[0]  # Table name is same as file name without extension

            # Create table if it does not exist
            with open(file_path, 'r') as f:
                header = next(csv.reader(f))
                create_query = f"CREATE TABLE dashboard_raw.{table_name} ({', '.join([col + ' TEXT' for col in header])});"
                cur.execute(create_query)

conn.commit()
cur.close()