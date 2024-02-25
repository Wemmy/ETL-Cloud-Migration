import redis,json
from datetime import datetime

r = redis.Redis(host="localhost", port=6379, db=0)

# Function to get data from Redis
def get_data_from_redis(selected_topic):
    keys = [key.decode('utf-8') for key in r.keys('*')]  # Get all keys and decode them to strings
    relevant_keys = [key for key in keys if selected_topic in key]  # Find keys containing the symbol
    all_data = []
    for key in relevant_keys:
        data = r.get(key)
        if data:
            all_data.extend(json.loads(data))
    return all_data

# Display data in Streamlit
def sort_data(symbol):
    data_list = get_data_from_redis(symbol)
    # Sort data list by date in descending order
    data_list.sort(key=lambda x: datetime.strptime(x['time_published'], "%Y%m%dT%H%M%S"), reverse=True)
    return data_list
