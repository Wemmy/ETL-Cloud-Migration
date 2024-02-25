import requests

def get_top_gainer_loser():
    pass

def get_news(API_KEY, topic, time_from):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topic}&apikey={API_KEY}&time_from={time_from}'
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


def get_real_gdp(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_real_gdp_per_capita(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_treasury_yield(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey={key}'
    r = requests.get(url)
    data = r.json() 
    return data

def get_fed_fund_rate(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_cpi(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_inflation(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=INFLATION&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_retail_sales(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_durables(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=DURABLES&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_unemployment_rate(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_nonfarm_payroll(key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_income_statements(symbol,key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data
def get_balance_sheet(symbol,key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data

def get_cash_flow(symbol,key):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey=={key}'
    r = requests.get(url)
    data = r.json()
    return data