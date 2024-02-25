import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date
import numpy as np
from plotly import graph_objs as go
from stocknews import StockNews
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.expected_returns import ema_historical_return
from pypfopt.risk_models import exp_cov
from pypfopt.efficient_frontier import EfficientFrontier


st.markdown('Page 1')
st.sidebar.markdown('Page 1')

# Setting time constraint
start = '2018-01-01'
today = date.today().strftime('%Y-%m-%d')

# Adding title, sidebar, etc
st.title('Minimum Viable Product')

# List of available stocks
stocks = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'NVDA',  'META', 'TSLA', 'AMD', 'GME', 'CSCO']
select_stocks = st.multiselect("Please select at least two Stocks", stocks)

if len(select_stocks) < 2:
    sys.exit()

# Adding a benchmark
benchmark_symbol = '^GSPC'
benchmark_data = yf.download(benchmark_symbol, start=start, end=today)

@st.cache_resource
def load_data(ticker):
    data = yf.download(ticker, start=start, end=today)
    sp_index = yf.download('^GSPC', start=start, end=today)
    return data,sp_index

# # Plotting the graph with percent change calculations
# st.subheader('Price Movements')
# data = load_data(select_stocks)
# data2 = data_load.copy()
# data2['% Change'] = data2['Close'] / data_load['Close'].shift(1) - 1
# st.write(data2.tail())
# st.write(benchmark_data.tail())

# Adding benchmark data to compare
# benchmark_data2 = benchmark_data.copy()
# benchmark_data2['% Change'] = benchmark_data2['Close'] / benchmark_data2['Close'].shift(1) - 1
st.subheader('Portfolio Performance with Evenly distribution')
data,sp_index = load_data(select_stocks)
portfolio_returns = data['Adj Close'].pct_change().dropna()
# port_comps_rets_cumprod = portfolio_returns.add(1).cumprod().sub(1)*100
test = portfolio_returns.dot(np.ones(len(portfolio_returns.columns)) / len(portfolio_returns.columns)).add(1).cumprod().subtract(1).multiply(100)
ind_ret = sp_index['Adj Close'].pct_change().dropna().add(1).cumprod().subtract(1).multiply(100)

back = pd.DataFrame({"Evenly Distributed":test, "SP500":ind_ret})
back.interpolate(method = "linear", inplace = True)
fig = px.line(back, x = back.index, y = back.columns)
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Cumulative Return in %')

# fig = px.line(port_comps_rets_cumprod,
#               x=port_comps_rets_cumprod.index,
#               y=port_comps_rets_cumprod.columns,
#               title='Cumulative Returns of Portfolio Stocks (2018-2023)')

fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Cumulative Return in %')
st.plotly_chart(fig)

# ########### Annual Return
# st.subheader('Annual Return')
# annual_return = data2['% Change'].mean() * 252 * 100
# st.write('Annual Return represents the percentage change in the investments value over a one-year period. In this context, it indicates that the investment has grown/shrunk by', round(annual_return, 2), '%', 'on an annual basis.')

# ########### Standard Deviation
# st.subheader('Standard Deviation')
# stdev = np.std(data2['% Change']) * np.sqrt(252)
# st.write('Standard Deviation is a measure of the amount of variation or dispersion in a set of values. In the context of financial investments, a higher standard deviation indicates a higher level of risk or volatility. Here, ', round(stdev * 100, 2), '%', 'represents the degree of fluctuation in the investments returns.')

# ########### Risk Return
# st.subheader('Risk Return')
# st.write('Risk-Return Ratio, also known as the Sharpe Ratio, is a measure of the relationship between the risk (as measured by standard deviation) and the return of an investment. A ratio close to 1 suggests a balanced relationship between risk and return. In this case, a ratio of: ', round(annual_return / (stdev * 100), 2))


train = portfolio_returns[:"2021-05-30"]
test = portfolio_returns["2021-05-31":]
mu = expected_returns.ema_historical_return(train, returns_data = True, span = 500)
sigma = risk_models.exp_cov(train, returns_data = True, span = 180)


# ef
ret_ef = np.arange(0, max(mu), 0.01)
vol_ef = []
for i in np.arange(0, max(mu), 0.01):
    ef = EfficientFrontier(mu, sigma)
    ef.efficient_return(i)
    vol_ef.append(ef.portfolio_performance()[1])

ef = EfficientFrontier(mu, sigma)
ef.min_volatility()
min_vol_ret = ef.portfolio_performance()[0]
min_vol_vol = ef.portfolio_performance()[1]

ef = EfficientFrontier(mu, sigma)
ef.max_sharpe(risk_free_rate=0.05)
max_sharpe_ret = ef.portfolio_performance()[0]
max_sharpe_vol = ef.portfolio_performance()[1]

st.subheader('Efficient Frontier')
# Create a figure with Plotly
fig = go.Figure()
# Adding the Efficient Frontier line plot
fig.add_trace(go.Scatter(x=vol_ef, y=ret_ef, mode='lines', name='Efficient Frontier'))
# Adding scatter plot for Minimum Variance Portfolio
fig.add_trace(go.Scatter(x=[min_vol_vol], y=[min_vol_ret], mode='markers', name='Minimum Variance Portfolio',
                         marker=dict(color='purple', size=10)))

# Adding scatter plot for Maximum Sharpe Portfolio
fig.add_trace(go.Scatter(x=[max_sharpe_vol], y=[max_sharpe_ret], mode='markers', name='Maximum Sharpe Portfolio',
                         marker=dict(color='green', size=10)))

# Adding the Capital Market Line
# fig.add_trace(go.Scatter(x=[0, max_sharpe_vol, 1], y=[0.05, max_sharpe_ret, 3.096], mode='lines', name='Capital Market Line',
#                          line=dict(color='red')))
# Update layout
fig.update_layout(
                  xaxis_title='Volatility', yaxis_title='Mean Return',
                  xaxis=dict(range=[0, 0.4]), yaxis=dict(range=[0, 1]),
                  legend_font_size=20)
st.plotly_chart(fig)



def draw_ticker_distribution(weight):
    # Assuming 'weights' is your dictionary of data
    desc = sorted(weight.items(), key=lambda x: x[1], reverse=True)
    labels = [i[0] for i in desc]
    vals = [i[1] for i in desc]
    # Create a horizontal bar chart
    fig = go.Figure(go.Bar(
        x=vals,
        y=labels,
        orientation='h'  # Horizontal bar chart
    ))
    # Update layout
    fig.update_layout(
        xaxis_title="Weight",
        yaxis=dict(autorange="reversed") # To invert the y-axis
    )
    st.plotly_chart(fig)



# Minimum Variance
st.subheader('Portfolio Distritubtion with Minimum Variance')
ef = EfficientFrontier(mu, sigma)
raw_weights_minvar_exp = ef.min_volatility()
draw_ticker_distribution(raw_weights_minvar_exp)

# Maximum Sharpe
st.subheader('Portfolio Distritubtion with Max return')
ef = EfficientFrontier(mu, sigma)
raw_weights_maxsharpe_exp = ef.max_sharpe(risk_free_rate=0.05)
draw_ticker_distribution(raw_weights_maxsharpe_exp)









# ########## Plotting the data
# def plot_raw_data(load_data, benchmark_data):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Close'], name=f'{select_stocks} Close'))
#     # fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Close'], name=f'{benchmark_symbol} Close'))
#     fig.update_layout(title_text='Time Series Data', xaxis_rangeslider_visible=True)
#     st.plotly_chart(fig)

# # plot_raw_data(data_load, benchmark_data)

# st.markdown('Page 2')
# st.sidebar.markdown('Page 2')
# st.title('Financial Analysis')

# benchmark_data['% Change'] = benchmark_data['Close'].pct_change()
# bench_ret = benchmark_data['% Change']
# bench_dev = (bench_ret + 1).cumprod()-1


# # Adding a subplot for cumulative return
# def plot_cumulative_return(stock_data, benchmark_data):
#     fig = go.Figure()

#     # Calculate cumulative return of the selected stock
#     stock_data['Cumulative Return'] = (1 + stock_data['% Change']).cumprod() - 1

#     # Calculate cumulative return of the benchmark
#     benchmark_data['Cumulative Return'] = (1 + benchmark_data['% Change']).cumprod() - 1

#     # Plotting cumulative return of the selected stock
#     fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Cumulative Return'], name=f'{select_stocks} Cumulative Return'))
#     # Plotting cumulative return of the benchmark
#     fig.add_trace(go.Scatter(x=benchmark_data.index, y=benchmark_data['Cumulative Return'], name=f'{benchmark_symbol} Cumulative Return'))
#     fig.update_layout(title_text='Cumulative Return Comparison', xaxis_rangeslider_visible=True)
#     st.plotly_chart(fig)

# # plot_cumulative_return(data2, benchmark_data2)


# # Fetching the latest 5 news for the selected stock
# st.header(f'News of {select_stocks}')
# sn = StockNews(select_stocks)
# df_news = sn.read_rss()
# # Displaying the news in a loop
# for i in range(10):
#     st.subheader(f'News {i + 1}')
#     st.write(f"Published: {df_news['published'][i]}")
#     st.write(f"Title: {df_news['title'][i]}")
#     st.write(f"Summary: {df_news['summary'][i]}")