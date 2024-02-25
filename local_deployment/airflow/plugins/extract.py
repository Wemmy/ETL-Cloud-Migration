from datetime import datetime, timedelta
from fmp import fmp_data
import os
from alpha import *
import json

def get_key(current_date):
    KEY = (
        current_date.strftime("%Y-%m-%d")
    )
    return KEY

def get_daily_data(API_KEY_FMP, API_KEY_ALPHA, stocklist):
    current_date = datetime.now()
    yesterday_date = current_date - timedelta(days=1)
    yesterday_date_formated = yesterday_date.strftime('%Y-%m-%d')
    d = fmp_data(API_KEY_FMP)
    month = current_date.strftime('%Y-%m')

    for stock in stocklist:
        # get historical stock price of over past 5 years
        data = d.get_historical_data(stock, to=yesterday_date_formated, **{'from': yesterday_date_formated})
        if len(data) > 0:
            # save it to json
            d.save_to_local(
                data, 
                os.path.join('/opt/airflow/data', 'raw', month, get_key(current_date), 'eod'), 
                f'{stock}.json', save_type = 'json'
            )

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

    # sentimental news
    # set file name and save the data
    file_path = os.path.join('/opt/airflow/data','raw', month, get_key(current_date), "news")
    # create data folder
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    timefrom = yesterday_date.strftime('%Y%m%dT%H%M')
    for t in topics:
        news = get_news(API_KEY_ALPHA, t, timefrom)
        file_name = os.path.join(file_path, f'{t}.json')
        json.dump(news, open(file_name, 'w'))