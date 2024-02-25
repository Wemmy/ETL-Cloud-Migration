import psycopg2
import csv
import os
import redis
import json
from datetime import datetime, timedelta
from utils import *

# datekey
current_date = datetime.now()
yesterday_date = current_date - timedelta(days=1)
yesterday_date_formated = yesterday_date.strftime('%Y-%m-%d')
month = current_date.strftime('%Y-%m')


def daily_load():

    db_details = {
        'dbname': 'postgres',
        'user': 'airflow',
        'password': 'airflow',
        'host': 'postgres',  # or your database host
        # 'port': '5432'
        }
    
    folder_path_pg = os.path.join('/opt/airflow/data', 'transformed', month, get_key(current_date))
    conn = psycopg2.connect(**db_details)
    cur = conn.cursor()
    for subdir, _, files in os.walk(folder_path_pg):
        for file in files:
            if file.endswith('eod.csv'):
                file_path = os.path.join(subdir, file)
                table_name = os.path.splitext(file)[0]  # Table name is same as file name without extension

                # Check if table exists
                cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = %s);", (table_name,))
                if not cur.fetchone()[0]:
                    # Create table if it does not exist
                    with open(file_path, 'r') as f:
                        header = next(csv.reader(f))
                        create_query = f"CREATE TABLE {table_name} ({', '.join([col + ' TEXT' for col in header])});"
                        cur.execute(create_query)

                # Insert data into table
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip the header row
                    for row in reader:
                        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
                        cur.execute(insert_query, row)
    conn.commit()
    cur.close()

    # load news
    topics = [
        'earnings',
        'ipo',
        'mergers_and_acquisitions',
        'financial_markets',
        'economy_fiscal',
        'economy_monetary',
        'economy_macro',
        'energy_transportation',
        'finance',
        'life_sciences',
        'manufacturing',
        'real_estate',
        'retail_wholesale',
        'technology'
    ]
    # Connect to Redis
    r = redis.Redis(host='redis', port=6379, db=0)

    for t in topics:
        file_name = os.path.join('/opt/airflow/data', 'raw',  month, get_key(current_date), 'news', f'{t}.json')
        with open(file_name, 'r') as f:
            data = json.load(f)
            # Extract the 'feed' part
            content = data.get('feed')
            # Serialize and store data
            serialized_data = json.dumps(content)
            if serialized_data is not None:
                if r.exists(t):
                    r.append(t, serialized_data)
                else:
                    r.set(t, serialized_data)



