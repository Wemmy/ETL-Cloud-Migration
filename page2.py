import streamlit as st
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date
import numpy as np
from plotly import graph_objs as go
import requests

def app():
    # st.title('Page 2')
    # st.write("This is Page 2")

    # Setting time constraint
    start = '2018-01-01'
    today = date.today().strftime('%Y-%m-%d')

    # Adding title, sidebar, etc
    st.title('Markets')

    # List of available stocks
    stocks = ['AAPL', 'MSFT', 'GME', 'F', 'TM', 'GOOG']
    select_stocks = st.selectbox("Pick a Stock", stocks)

    # Adding a benchmark
    benchmark_symbol = '^GSPC'
    benchmark_data = yf.download(benchmark_symbol, start=start, end=today)

    @st.cache_resource
    def load_data(ticker):
        data = yf.download(ticker, start=start, end=today)
        data.reset_index(inplace=True)
        return data

    # Plotting the graph with percent change calculations
    st.subheader('Price Movements')
    data_load = load_data(select_stocks)
    data2 = data_load.copy()
    data2['% Change'] = data2['Close'] / data_load['Close'].shift(1) - 1
    st.write(data2.tail())

    # st.write(benchmark_data.tail())

    # Adding benchmark data to compare
    benchmark_data2 = benchmark_data.copy()
    benchmark_data2['% Change'] = benchmark_data2['Close'] / benchmark_data2['Close'].shift(1) - 1

    ########### Annual Return
    st.subheader('Annual Return')
    annual_return = data2['% Change'].mean() * 252 * 100
    st.write('Annual Return represents the percentage change in the investments value over a one-year period. In this context, it indicates that the investment has grown/shrunk by', round(annual_return, 2), '%', 'on an annual basis.')

    ########### Standard Deviation
    st.subheader('Standard Deviation')
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is a measure of the amount of variation or dispersion in a set of values. In the context of financial investments, a higher standard deviation indicates a higher level of risk or volatility. Here, ', round(stdev * 100, 2), '%', 'represents the degree of fluctuation in the investments returns.')

    ########### Risk Return
    st.subheader('Risk Return')
    st.write('Risk-Return Ratio, also known as the Sharpe Ratio, is a measure of the relationship between the risk (as measured by standard deviation) and the return of an investment. A ratio close to 1 suggests a balanced relationship between risk and return. In this case, a ratio of: ', round(annual_return / (stdev * 100), 2))

    ########## Plotting the data
    def plot_raw_data(load_data, benchmark_data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Close'], name=f'{select_stocks} Close'))
        # fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Close'], name=f'{benchmark_symbol} Close'))
        fig.update_layout(title_text='Time Series Data', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data(data_load, benchmark_data)


    st.title('Benchmark Comparison')



    benchmark_data['% Change'] = benchmark_data['Close'].pct_change()
    bench_ret = benchmark_data['% Change']
    bench_dev = (bench_ret + 1).cumprod()-1
    # Adding a subplot for cumulative return
    def plot_cumulative_return(stock_data, benchmark_data):
        fig = go.Figure()

        # Calculate cumulative return of the selected stock
        stock_data['Cumulative Return'] = (1 + stock_data['% Change']).cumprod() - 1

        # Calculate cumulative return of the benchmark
        benchmark_data['Cumulative Return'] = (1 + benchmark_data['% Change']).cumprod() - 1

        # Plotting cumulative return of the selected stock
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Cumulative Return'], name=f'{select_stocks} Cumulative Return'))

        # Plotting cumulative return of the benchmark
        fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Cumulative Return'], name=f'{benchmark_symbol} Cumulative Return'))

        fig.update_layout(title_text='Cumulative Return Comparison', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_cumulative_return(data2, benchmark_data2)





    st.title('Income Statement')
    # Function to retrieve income statement data
    def get_income_data(stock):
        base_url = 'https://financialmodelingprep.com/api'
        data_type = 'income-statement'
        API_KEY = 'mJfaCAPHiFiGPEPUx4mcft0V2fLcOueo'
        
        url = f'{base_url}/v3/{data_type}/{stock}?period=annual&apikey={API_KEY}'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.error(f"Failed to fetch income statement data for {stock}. Please check the stock symbol.")

    # Fetching income statement data for the selected stock
    income_data = get_income_data(select_stocks)

    if income_data is not None and not income_data.empty:
        # Print the entire DataFrame
        revenue_data = income_data['revenue']
        net_income_data = income_data['netIncome']
        cost_revenue = income_data['costOfRevenue']
        net_income_ratio_data = income_data['netIncomeRatio'] * 100  # Scale it to make it more visible
        years = income_data['calendarYear']

        # Plotting revenue and net income as bar plots
        fig = go.Figure()

        # Bar plot for revenue
        fig.add_trace(go.Bar(x=years, y=revenue_data, name='Revenue'))
        # # Bar plot for expenses
        fig.add_trace(go.Bar(x=years, y=cost_revenue, name='Cost of Revenue'))
        # Bar plot for net income
        fig.add_trace(go.Bar(x=years, y=net_income_data, name='Net Income'))
        # Line plot for net income ratio with a separate y-axis
        fig.add_trace(go.Scatter(x=years, y=net_income_ratio_data, mode='lines', name='Net Income Ratio', yaxis='y2'))

        # Add a secondary y-axis
        fig.update_layout(
            # title_text='Growth and Profitability',
            xaxis_title='Year',
            yaxis_title='Values',
            yaxis2=dict(title='Net Income Ratio (%)', overlaying='y', side='right', showgrid=False),
            legend=dict(x=1.2, y=1.0)  # Adjust the legend position
        )

        st.plotly_chart(fig)

    st.title('Financial health')
    def get_health_data(stock):
        base_url = 'https://financialmodelingprep.com/api'
        data_type = 'balance-sheet-statement'
        API_KEY='mJfaCAPHiFiGPEPUx4mcft0V2fLcOueo'


        url = f'{base_url}/v3/{data_type}/{stock}?period=annual&apikey={API_KEY}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
    # Fetching income statement data for the selected stock
    health_data = get_health_data(select_stocks)

    # st.write(health_data)
    # st.write(assets_data)
    if income_data is not None and not income_data.empty:
        # Print the entire DataFrame
        assets_data = health_data['totalAssets']
        liabilities_data = health_data['totalLiabilities']
        years = health_data['calendarYear']

        fig2 = go.Figure()
        # Bar plot for revenue
        fig2.add_trace(go.Bar(x=years, y=assets_data, name='Total Assets'))
        # Bar plot for expenses
        fig2.add_trace(go.Bar(x=years, y=liabilities_data, name='Total Liabilities'))

        st.plotly_chart(fig2)









