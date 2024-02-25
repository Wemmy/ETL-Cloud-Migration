import json
from const import stocklist, API_KEY
from get_data_fmp import fmp_data
from get_data_alpha import *
import os
from botocore.exceptions import ClientError
from datetime import datetime,timedelta

def get_raw_data(API_KEY, stocklist):
    # monthly update metrics
    # Get the current date
    current_date = datetime.now()
    yesterday_date = current_date - timedelta(days=1)
    # Calculate yesterday's date
    yesterday_date_formated = yesterday_date.strftime('%Y-%m-%d')
    # Format dates in 'yyyy-mm-dd'
    formatted_today = current_date.strftime('%Y-%m-%d')
    # formatted_yesterday = yesterday_date.strftime('%Y-%m-%d')

    month = current_date.strftime('%Y-%m')

    d = fmp_data(API_KEY)
    buket_name =os.environ.get('S3_BUCKET_NAME')

    for stock in stocklist:
        # get historical stock price of over past 5 years
        data = d.get_historical_data(stock, to=yesterday_date_formated, **{'from': yesterday_date_formated})
        if len(data) > 0:
            # save it to json
            d.write_json_to_s3(
                data, 
                buket_name, 
                os.path.join(month, d._get_key(), 'eod', f'{stock}.json')
                )
            
    timefrom = yesterday_date.strftime('%Y%m%dT%H%M')
    # sentimental news
    news = get_news(timefrom)
    write_json_to_s3(news, buket_name, os.path.join(month, d._get_key(), f'news.json'))

    
    # Check if today is the first day of the month
    if current_date.day == 1:
        write_json_to_s3(get_real_gdp(), buket_name, os.path.join('metrics', 'real_gdp.json'))
        write_json_to_s3(get_real_gdp_per_capita(), buket_name, os.path.join('metrics', 'real_gdp_per_capita.json'))
        write_json_to_s3(get_treasury_yield(), buket_name, os.path.join( 'metrics', 'treasury_yield.json'))
        write_json_to_s3(get_fed_fund_rate(), buket_name, os.path.join( 'metrics', 'fed_fund_rate.json'))
        write_json_to_s3(get_cpi(), buket_name, os.path.join('metrics', 'cpi.json'))
        write_json_to_s3(get_inflation(), buket_name, os.path.join( 'metrics', 'inflation.json'))
        write_json_to_s3(get_retail_sales(), buket_name, os.path.join( 'metrics', 'retail_sales.json'))
        write_json_to_s3(get_durables(), buket_name, os.path.join( 'metrics', 'durables.json'))
        write_json_to_s3(get_unemployment_rate(), buket_name, os.path.join( 'metrics', 'unemployment_rate.json'))
        write_json_to_s3(get_nonfarm_payroll(), buket_name, os.path.join( 'metrics', 'nonfarm_payroll.json'))

        # yearly metrics
        for stock in stocklist:
            # get income_statement
            data = d.get_income_statements(stock, period='annual')
            # save it to json
            d.write_json_to_s3(
                data, 
                buket_name, 
                os.path.join('metrics', 'income_statement', f'{stock}.json')
                )

            # get fuill financial statements
            data = d.get_balance_sheet_statement(stock, period='annual')
            # save it to json
            d.write_json_to_s3(
                data, 
                buket_name, 
                os.path.join('metrics', 'balance_sheet_statement', f'{stock}.json')
                )

            # get fuill financial statements
            data = d.get_cashflow_statements(stock, period='annual')
            # save it to json
            d.write_json_to_s3(
                data, 
                buket_name, 
                os.path.join('metrics', 'cashflow_statement', f'{stock}.json')
                )

            # get fuill financial statements
            data = d.get_key_metrics(stock, period='annual')
            # save it to json
            d.write_json_to_s3(
                data, 
                buket_name, 
                os.path.join('metrics', 'key_metrics', f'{stock}.json')
                )
    
def lambda_handler(event, context):
    try:
        get_raw_data(API_KEY, stocklist)

        # If everything goes well
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Function executed successfully",
                # Include any additional response data here
            })
        }
    except Exception as e:
        # Handle any exceptions that occur
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "An error occurred",
                "error": str(e),
                # Include any additional error information here
            })
        }

