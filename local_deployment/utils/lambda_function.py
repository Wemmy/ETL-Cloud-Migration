import boto3
from datetime import datetime, timezone,timedelta
import json
import os
from urllib.request import urlopen
import certifi

s3_client = boto3.client("s3")
LOCAL_FILE_SYS = "./data"
S3_BUCKET = "your-s3-bucket"  # please replace with your bucket name
CHUNK_SIZE = 10000  # determined based on API, memory constraints, experimentation


def _get_key():
    dt_now = datetime.now(tz=timezone.utc)
    KEY = (
        dt_now.strftime("%Y-%m-%d")
        + "/"
        + dt_now.strftime("%H")
        + "/"
        + dt_now.strftime("%M")
        + "/"
    )
    return KEY

def get_num_records():
    # Dummy function, to replicate GET http://jsonplaceholder.typicode.com/number_of_users call
    return 100000

def get_data(
    start_date, end_date, stock, apikey, get_path="https://financialmodelingprep.com/api/v3/historical-price-full/"
):
    url = f'{get_path}{stock}?apikey={apikey}&from={start_date}&to={end_date}'
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode('utf-8')
    return json.loads(data)

# def parse_data(json_data):
#     return f'{json_data.get("userId")},{json_data["id"]},"{json_data["title"]}"\n'

def write_to_local(data, folder_path, file_name, loc=LOCAL_FILE_SYS):
    f = os.path.join(folder_path, file_name)
    with open(f, "w") as file:
        json.dump(data, file)
    print(f'write to {f}')

def _iter_period(start_date = '2018-12-01', end_date = '2023-12-01', month_step=12):
    periods = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    while current_date < end_date:
        # Calculate the end date of the period
        year = current_date.year + ((current_date.month + month_step - 1) // 12)
        month = (current_date.month + month_step - 1) % 12 + 1
        day = min(current_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        next_date = datetime(year, month, day)
        # Adjust the end date if it exceeds the overall end date
        period_end = min(next_date, end_date)
        if period_end < end_date:
            # Subtract one day from the period_end date
            period_end = period_end - timedelta(days=1)
        # Add the period as a tuple
        # periods.append((current_date.strftime('%Y-%m-%d'), period_end.strftime('%Y-%m-%d')))
        yield (current_date.strftime('%Y-%m-%d'), period_end.strftime('%Y-%m-%d'))
        # Update the current date for the next iteration
        current_date = period_end + timedelta(days=1)
    print(periods)

def download_past5year_data(apikey, stock = 'MSFT'):
    '''
    DOWN LOAD FILE TO LOCAL
    '''
    for start_date, end_date in _iter_period():
        data = get_data(start_date, end_date, apikey, stock)
        folder = f'{stock}'
        folder_path = os.path.join(LOCAL_FILE_SYS, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = str(datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')) + '_' + str(datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')) + '.json'
        write_to_local(data, folder_path, file_name)

# def lambda_handler(event, context):
#     N = get_num_records()
#     download_data(N)
#     key = _get_key()
#     files = [f for f in listdir(LOCAL_FILE_SYS) if isfile(join(LOCAL_FILE_SYS, f))]
#     for f in files:
#         s3_client.upload_file(LOCAL_FILE_SYS + "/" + f, S3_BUCKET, key + f)


if __name__ == "__main__":
    pass



