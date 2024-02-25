import requests,os,json

API_KEY = os.getenv('ALPHA_API_KEY')

def get_top_gainer_loser():
    pass

path_topics = os.path.join('data', 'raw', 'topics')
def get_and_save_news(topic, path):
    '''
    get the topic json data ans save to path
    '''
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topic}&apikey={API_KEY}&limit=1000'
    r = requests.get(url)
    data = r.json()

    # create data folder
    if not os.path.exists(path):
        os.makedirs(path)

    # set file name and save the data
    file_name = os.path.join(path, f'{topic}.json')
    json.dump(data, open(file_name, 'w'))

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

def get_topics():
    for topic in topics:
        get_and_save_news(topic, path_topics)

def get_real_gdp(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()



    # set file name and save the data
    file_name = os.path.join(path, 'gdp.json')
    json.dump(data, open(file_name, 'w'))

def get_real_gdp_per_capita(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    # set file name and save the data
    file_name = os.path.join(path, 'gdp_per_capita.json')
    json.dump(data, open(file_name, 'w'))

def get_treasury_yield(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json() 

    

    # set file name and save the data
    file_name = os.path.join(path, 'treasury_yield.json')
    json.dump(data, open(file_name, 'w'))

def get_fed_fund_rate(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    

    # set file name and save the data
    file_name = os.path.join(path, 'fed_fund_rate.json')
    json.dump(data, open(file_name, 'w'))

def get_cpi(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    

    # set file name and save the data
    file_name = os.path.join(path, 'cpi.json')
    json.dump(data, open(file_name, 'w'))

def get_inflation(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=INFLATION&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    # set file name and save the data
    file_name = os.path.join(path, 'inflation.json')
    json.dump(data, open(file_name, 'w'))

def get_retail_sales(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()  

    # set file name and save the data
    file_name = os.path.join(path, 'retail_sales.json')
    json.dump(data, open(file_name, 'w'))

def get_durables(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=DURABLES&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    

    # set file name and save the data
    file_name = os.path.join(path, 'durables.json')
    json.dump(data, open(file_name, 'w'))

def get_unemployment_rate(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    # set file name and save the data
    file_name = os.path.join(path, 'unemployment.json')
    json.dump(data, open(file_name, 'w'))

def get_nonfarm_payroll(path):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=={API_KEY}'
    r = requests.get(url)
    data = r.json()

    # set file name and save the data
    file_name = os.path.join(path, 'nonfarm_payroll.json')
    json.dump(data, open(file_name, 'w'))

path_indicator = os.path.join('alpha', 'data', 'indicator')

def get_indicator():
    get_real_gdp(path_indicator)
    get_real_gdp_per_capita(path_indicator)
    get_treasury_yield(path_indicator)
    get_fed_fund_rate(path_indicator)
    get_cpi(path_indicator)
    get_inflation(path_indicator)
    get_retail_sales(path_indicator)
    get_durables(path_indicator)
    get_unemployment_rate(path_indicator)
    get_nonfarm_payroll(path_indicator)