import psycopg2
import csv
import os
import redis
import json

folder_path_pg = os.path.join('data', 'transformed')

def load_csv_to_postgres(folder_path, db_details):
    """
    Load all CSV files from a folder into a PostgreSQL database. If a table does not exist, create it.

    :param folder_path: The path to the folder containing CSV files.
    :param db_details: A dictionary containing database details like dbname, user, password, host, port.
    """
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**db_details)
        cur = conn.cursor()
        for subdir, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.csv'):
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

    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
    
# Example usage
db_details = {
    'dbname': 'postgres',
    'user': 'airflow',
    'password': 'airflow',
    'host': '127.0.0.1',  # or your database host
    'port': '5432'
}

load_csv_to_postgres(folder_path_pg, db_details)  

'''
test
'''
# folder_path_redis = os.path.join('data', 'raw', 'news')
# def load_json_content_to_redis(folder_path, redis_host='localhost', redis_port=6379, redis_db=0):
#     """
#     Load the 'content' from each JSON file in the folder into a single Redis key.

#     :param folder_path: Path to the folder containing JSON files.
#     :param redis_key: The Redis key under which the data will be stored.
#     :param redis_host: Hostname of the Redis server.
#     :param redis_port: Port of the Redis server.
#     :param redis_db: Redis database number.
#     """
#     # Connect to Redis
#     r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

#     for file in os.listdir(folder_path):
#         if file.endswith('.json'):
#             file_path = os.path.join(folder_path, file)
#             with open(file_path, 'r') as f:
#                 data = json.load(f)
#                 # Extract the 'content' part
#                 content = data.get('content')  # This gets the list of articles
#                 # extrack news
#                 for item in content:
#                     # Split the tickers and process each one
#                     tickers = item['tickers'].split(', ')
#                     for ticker in tickers:
#                         # Retrieve existing data for the ticker, append new item, and save back to Redis
#                         existing_data = r.get(ticker)
#                         if existing_data:
#                             existing_data = json.loads(existing_data)
#                         else:
#                             existing_data = []
#                         existing_data.append(item)
#                         r.set(ticker, json.dumps(existing_data))
# load_json_content_to_redis(folder_path_redis)
'''
test
'''

# LOAD TOPIC DATA
def load_json_content_to_redis(topic, redis_host='localhost', redis_port=6379, redis_db=0):
    file_name = os.path.join('data', 'raw', 'topics',  f'{topic}.json')
    # Connect to Redis
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    with open(file_name, 'r') as f:
        data = json.load(f)
        # Extract the 'feed' part
        content = data.get('feed')
        # Serialize and store data
        serialized_data = json.dumps(content)
        r.set(topic, serialized_data)

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

for topic in topics:
    load_json_content_to_redis(topic)

def get_largest_smallest_sentiment_score(topics, redis_host='localhost', redis_port=6379, redis_db=0):
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    # get the largets     
    max_score = float('-inf')
    min_score = float('inf')
    # Iterate over each key
    for key in topics:
        # Fetch and deserialize data
        serialized_data = r.get(key)
        if serialized_data:
            data_list = json.loads(serialized_data)
            # Find max and min in current list
            for item in data_list:
                score = item.get('overall_sentiment_score')
                if score is not None:
                    max_score = max(max_score, score)
                    min_score = min(min_score, score)

    # Check if any scores were found
    if max_score == float('-inf') or min_score == float('inf'):
        print("No scores found.")
    else:
        print(f"Largest Score: {max_score}")
        print(f"Smallest Score: {min_score}")

# get_largest_smallest_sentiment_score(topics)
# folder_path_pg = os.path.join('alpha', 'data', 'transformed')
# def load_csv_to_postgres_2(folder_path, db_details):
#     """
#     Load all CSV files from a folder into a PostgreSQL database. If a table does not exist, create it.

#     :param folder_path: The path to the folder containing CSV files.
#     :param db_details: A dictionary containing database details like dbname, user, password, host, port.
#     """
#     try:
#         # Connect to PostgreSQL database
#         conn = psycopg2.connect(**db_details)
#         cur = conn.cursor()

#         for subdir, _, files in os.walk(folder_path):
#             for file in files:
#                 if file.endswith('.csv'):
#                     file_path = os.path.join(subdir, file)
#                     table_name = os.path.splitext(file)[0]  # Table name is same as file name without extension

#                     # Check if table exists
#                     cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = %s);", (table_name,))
#                     if not cur.fetchone()[0]:
#                         # Create table if it does not exist
#                         with open(file_path, 'r') as f:
#                             header = next(csv.reader(f))
#                             create_query = f"CREATE TABLE {table_name} ({', '.join([col + ' TEXT' for col in header])});"
#                             cur.execute(create_query)

#                         # Insert data into table
#                         with open(file_path, 'r') as f:
#                             reader = csv.reader(f)
#                             next(reader)  # Skip the header row
#                             for row in reader:
#                                 insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
#                                 cur.execute(insert_query, row)
#         conn.commit()
#         cur.close()

#     except psycopg2.Error as e:
#         print(f"Error: {e}")
#     finally:
#         if conn:
#             conn.close()
# load_csv_to_postgres(folder_path_pg, db_details)  