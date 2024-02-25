from utils.fmp.get_data import get_raw_data
import os
from utils.alpha.extract import get_topics, get_indicator

stocklist = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'NVDA',  'META', 'TSLA', 'AMD', 'GME', 'CSCO']
API_KEY = os.getenv('FMP_API_KEY')
DATA_FOLDER = 'data'

if __name__ == '__main__':

    # download data if not exists
    if not os.path.exists('data'):
        get_raw_data(API_KEY, stocklist)

        get_topics()

        get_indicator()
    