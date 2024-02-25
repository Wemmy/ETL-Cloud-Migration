import certifi
import json
import os
from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import pandas as pd
from pandas import json_normalize
import pickle
import boto3

# Set API key
class fmp_data:

    def __init__(self, API_KEY, DATA_FOLDER='data') -> None:
        self.api_key = API_KEY
        self.base_url = 'https://financialmodelingprep.com/api'
        self.data_folder =  DATA_FOLDER

    # append api args
    def _build_url(self, *args, **kwargs):
        # add api_key
        kwargs['apikey'] = self.api_key

         # Join the base URL with the path elements
        url = self.base_url
        for path_element in args:
            url = urljoin(url + '/', str(path_element))

        # Append query parameters
        if kwargs:
            url += '?' + urlencode(kwargs)
        print(url)
        return url

    # time key
    # def _get_key():
    #     dt_now = datetime.now(tz=timezone.utc)
    #     KEY = (
    #         dt_now.strftime("%Y-%m-%d")
    #         + "/"
    #         + dt_now.strftime("%H")
    #         + "/"
    #         + dt_now.strftime("%M")
    #         + "/"
    #     )
    #     return KEY
    
    # get json data from url
    def _get_jsonparsed_data(self, url):
        try:
            response = urlopen(url, cafile=certifi.where())
            data = response.read().decode('utf-8')
        except Exception as e:
            raise e
        return json.loads(data)

    def get_symbol_list(self, **kwargs):
        '''
        [
            {
                "symbol": "PWP",
                "exchange": "NASDAQ Global Select",
                "exchangeShortName": "NASDAQ",
                "price": "8.13",
                "name": "Perella Weinberg Partners"
            }
        ]
        '''
        return self._get_jsonparsed_data(self._build_url('v3', 'stock', 'list' **kwargs))

    def get_statement_symbols_list(self, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'financial-statement-symbols-list' **kwargs))
    
    def get_tradable_search(self, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'available-traded', 'list' **kwargs))
    
    def get_available_indexes(self, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'symbol', 'available-indexes' **kwargs))
    
    def get_exchange_symbol(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'symbol', *args, **kwargs))

    def get_company_profile(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'profile', *args, **kwargs))

    def get_market_cap(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'market-capitalization', *args, **kwargs))

    def get_stock_screener(self, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'stock-screener', **kwargs))

    def get_company_rating(self, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'rating', **kwargs))
    
    def get_income_statements(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'income-statement', *args, **kwargs))
   
    def get_balance_sheet_statement(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'balance-sheet-statement', *args, **kwargs))
    
    def get_cashflow_statements(self,*args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'cash-flow-statement',*args, **kwargs))
 
    def get_full_financial_statements(self,*args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'financial-statement-full-as-reported',*args, **kwargs))
    
    def get_key_metrics(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'key-metrics',*args, **kwargs))

    def get_historical_data(self,*args, **kwargs):
        '''
        {
            "symbol": "AAPL",
            "historical": [
                {
                    "date": "2023-10-06",
                    "open": 173.8,
                    "high": 176.61,
                    "low": 173.18,
                    "close": 176.53,
                    "adjClose": 176.53,
                    "volume": 21712747,
                    "unadjustedVolume": 21712747,
                    "change": 2.73,
                    "changePercent": 1.57077,
                    "vwap": 175.44,
                    "label": "October 06, 23",
                    "changeOverTime": 0.0157077
                },
                {
                    "date": "2023-10-05",
                    "open": 173.79,
                    "high": 175.45,
                    "low": 172.68,
                    "close": 174.91,
                    "adjClose": 174.91,
                    "volume": 48251046,
                    "unadjustedVolume": 47369743,
                    "change": 1.12,
                    "changePercent": 0.64446,
                    "vwap": 174.23,
                    "label": "October 05, 23",
                    "changeOverTime": 0.0064446
                }
            ]
        }
        '''
        return self._get_jsonparsed_data(self._build_url('v3', 'historical-price-full',*args, **kwargs))

    def get_news(self, *args, **kwargs):
        return self._get_jsonparsed_data(self._build_url('v3', 'fmp','articles',*args, **kwargs))

    def save_to_local(self, data, file_path, file_name, save_type = 'json'):
        '''
        file name contains all path after ./data
        '''
        path = os.path.join(self.data_folder, file_path)

        # create data folder
        if not os.path.exists(path):
            os.makedirs(path)

        file_name = os.path.join(path, file_name)
        file_name, ext  = os.path.splitext(file_name)

        if save_type == 'json':
            file_name = file_name + '.json'
            json.dump(data, open(file_name, 'w'))
        elif save_type == 'parquet':
            file_name = file_name + '.parquet'
            self.json_to_parquet(data, file_name)
        elif save_type == 'pickle':
            file_name = file_name + '.pkl'
            pickle.dump(data, open(file_name, 'w'))
        else:
            raise Exception('Unknown type')


    @staticmethod
    def json_to_parquet(json_data, output_file):
        """
        Converts JSON data to a Parquet file.

        :param json_data: A string representing the JSON data or a path to a JSON file.
        :param output_file: Path where the output Parquet file will be stored.
        """
        # Read JSON data into a pandas DataFrame
        if isinstance(json_data, str):
            df = pd.read_json(json_data, lines=True)
        else:
            try:
                # Assuming json_data is already a Python dictionary
                df = pd.DataFrame(json_data)
            except TypeError as e:
                df = json_normalize(json_data)
        # Write DataFrame to a Parquet file
        df.to_parquet(output_file, index=False)
    
    @staticmethod
    def dict_to_parquet(data_dict, output_file):
        """
        Converts a dictionary to a Parquet file.

        :param data_dict: The dictionary to convert. Each key-value pair represents a column and its values.
        :param output_file: Path where the output Parquet file will be stored.
        """
        # Convert dictionary to DataFrame
        df = pd.DataFrame(data_dict)

        # Write DataFrame to Parquet file
        df.to_parquet(output_file, index=False)

    @staticmethod
    def write_json_to_s3(data, bucket_name, file_name):
        """
        Write JSON data directly to a file in an S3 bucket.

        Parameters:
        data (dict): JSON data to write.
        bucket_name (str): Name of the S3 bucket.
        file_name (str): File name to be used in the S3 bucket.
        aws_access_key_id (str): AWS access key id.
        aws_secret_access_key (str): AWS secret access key.
        aws_session_token (str, optional): AWS session token (if any).

        Returns:
        None
        """
        # Initialize the S3 client
        s3_client = boto3.client('s3')

        # Convert the data to JSON
        json_data = json.dumps(data)

        # Write the JSON data to the specified S3 bucket
        s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)


def get_raw_data(API_KEY, stocklist):

    d = fmp_data(API_KEY)

    for stock in stocklist:
        # get historical stock price of over past 5 years
        data_five_year = d.get_historical_data(stock)
        # save it to json
        d.save_to_local(data_five_year, os.path.join('raw', 'eod'), stock)

        # get income_statement
        data = d.get_income_statements(stock, period='annual')
        # save it to json
        d.save_to_local(data, os.path.join('raw','income_statement'), stock)

        # get fuill financial statements
        data = d.get_balance_sheet_statement(stock, period='annual')
        # save it to json
        d.save_to_local(data, os.path.join('raw','balance_sheet_statement'), stock)

        # get fuill financial statements
        data = d.get_cashflow_statements(stock, period='annual')
        # save it to json
        d.save_to_local(data, os.path.join('raw','cashflow_statement'), stock)

        # get fuill financial statements
        data = d.get_key_metrics(stock, period='annual')
        # save it to json
        d.save_to_local(data, os.path.join('raw','key_metrics'), stock)

    # news (total 3400 news as of 01/06/2024)
    for i in range(0,4):
        data = d.get_news(page = i, size = 1000)
        d.save_to_local(data, os.path.join('raw','news'), f'news_p{i}')


if __name__ == "__main__":
    pass

    