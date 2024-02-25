import yfinance as yf
import os
import pandas as pd

def get_historical_stock_data(tickers):
    tickers_list = tickers.split(' ')
    
    new_stock_cols = ['Ticker', 'Open', 'High', 'Low',
                      'Close', 'Adj Close', 'Volume']
    
    new_cashflow_cols = ['Ticker', 'Operating Cash Flow', 'Investing Cash Flow', 
                         'Financing Cash Flow', 'End Cash Position', 
                         'Capital Expenditure', 'Issuance Of Debt', 
                         'Repayment Of Debt', 'Free Cash Flow']
    
    for ticker in tickers_list:
        # Get stock price and cash flow history (dataframe)
        stock_df = yf.download(ticker, period='5y') 
        cashflow_df = yf.Ticker(ticker).cashflow

        # Add new column with ticker symbol and add dataframe to list
        stock_df['Ticker'] = ticker
        stock_frames.append(stock_df)

        # Set filename
        cashflow_filename = ticker + '_cashflow.csv'  
        
        # Get current lisf of cashflow columns
        curr_cashflow_cols = list(cashflow_df.index.values)
        
        # Get the index of the new columns in the current colums
        col_index = []
        
        for col in range(1, len(new_cashflow_cols)):
            col_index.append(curr_cashflow_cols.index(new_cashflow_cols[col]))
        
        # Recreate cashflow dataframe using the indices from the column index list   
        cashflow_df = cashflow_df.iloc[col_index,  :] 
        cashflow_df_trans = cashflow_df.transpose()   # Transpose dataframe
        cashflow_df_trans.index.name = 'Date'         # Rename index column  
        cashflow_df_trans['Ticker'] = ticker          # Add new column
        cashflow_frames.append(cashflow_df_trans)     # Add dataframe to the list of cashflow dataframes

    # Combine list of dataframes into one
    stocks_df = pd.concat(stock_frames) 
    cashflow_df_trans = pd.concat(cashflow_frames)
    
    # Rearrange cols
    stocks_df = stocks_df[new_stock_cols]
    cashflow_df_trans = cashflow_df_trans[new_cashflow_cols] 

    # Save stocks and cashflow as CSV
    stocks_df.to_csv('./data/stocks.csv', index=True) 
    cashflow_df_trans.to_csv('./data/cashflow.csv', index=True) 
    
    
if __name__ == "__main__":

    # Set working directory
    # os.chdir('ENTER YOUR WORKING DIRECTORY HERE')

    # Create list to append stock and cashflow dataframes
    stock_frames = []
    cashflow_frames = []

    # Get stock price and cashflow history
    tickers = 'MSFT AAPL GOOG AMZN NVDA META TSLA AMD GME CSCO'
    get_historical_stock_data(tickers)