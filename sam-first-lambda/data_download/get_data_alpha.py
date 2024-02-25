import requests,json, boto3
from const import KEY
key = KEY

def get_top_gainer_loser():
    pass

def get_news(time_from):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={key}&time_from={time_from}'
    r = requests.get(url)
    data = r.json()
    return data


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


def get_real_gdp():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_real_gdp_per_capita():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_treasury_yield():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={key}'
    r = requests.get(url)
    data = r.json() 
    return data

def get_fed_fund_rate():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_cpi():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_inflation():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=INFLATION&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_retail_sales():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_durables():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=DURABLES&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_unemployment_rate():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_nonfarm_payroll():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_income_statements(symbol):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data
def get_balance_sheet(symbol):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data
def get_cash_flow(symbol):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data

def write_json_to_s3(data, bucket_name, file_name):
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Convert the data to JSON
    json_data = json.dumps(data)

    # Write the JSON data to the specified S3 bucket
    s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)