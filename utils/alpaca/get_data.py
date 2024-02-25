from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from datetime import datetime
from alpaca.data.timeframe import TimeFrame
import os

KEY = os.getenv('ALPACA_API_KEY')
SECRET = os.getenv('ALPACA_SECRET')

ticers = ["AAPL", "MSFT"]
start_date = datetime(2023, 8, 1)
end_Date=datetime(2023, 9, 1)

stock_client = StockHistoricalDataClient(KEY,  SECRET)

request_params = StockBarsRequest(
                        symbol_or_symbols=ticers,
                        timeframe=TimeFrame.Day,
                        start=start_date,
                        end=end_Date
                 )
historical_data  = stock_client.get_stock_bars(request_params)