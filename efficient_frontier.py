import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta, date
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

def app():

    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    one_year_ago.strftime('%Y-%m-%d')
    # Setting time constraint
    # today = date.today().strftime('%Y-%m-%d')

    # Adding title, sidebar, etc
    st.title('Mean Variance Optimization')

    # List of available stocks
    # stocks = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'NVDA',  'META', 'TSLA', 'AMD', 'GME', 'CSCO']
    stocks = ['AAPL','MSFT',
    'META',
    'AMZN',
    'XOM',
    'UNH',
    'JNJ',
    'V',
    'HD',
    'ABBV',
    'KO',
    'DIS',
    'T',
    'UPS',
    'LMT',
    'CAT',
    'F',
    'MAR',
    'O',
    'HSY']
    select_stocks = st.multiselect("Please select at least two Stocks", stocks)

    if len(select_stocks) < 2:
        sys.exit()

    @st.cache_resource
    def load_data(ticker):
        data = yf.download(ticker, start=one_year_ago, end=today.strftime('%Y-%m-%d'))
        sp_index = yf.download('^GSPC', start=one_year_ago, end=today.strftime('%Y-%m-%d'))
        return data,sp_index

    data,sp_index = load_data(select_stocks)
    portfolio_returns = data['Adj Close'].pct_change().dropna()
    # port_comps_rets_cumprod = portfolio_returns.add(1).cumprod().sub(1)*100
    test = portfolio_returns.dot(np.ones(len(portfolio_returns.columns)) / len(portfolio_returns.columns)).add(1).cumprod().subtract(1).multiply(100)
    ind_ret = sp_index['Adj Close'].pct_change().dropna().add(1).cumprod().subtract(1).multiply(100)

    back = pd.DataFrame({"Evenly Distributed":test, "SP500":ind_ret})
    back.interpolate(method = "linear", inplace = True)

    st.subheader('Portfolio Performance with Even Distribution')
    fig = px.line(back, x = back.index, y = back.columns)
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Cumulative Return in %')

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Cumulative Return in %')
    st.plotly_chart(fig)

    # train = portfolio_returns[one_year_ago:]
    # test = portfolio_returns["2021-05-31":]
    train = portfolio_returns
    mu = expected_returns.ema_historical_return(train, returns_data = True, span = 500)
    sigma = risk_models.exp_cov(train, returns_data = True, span = 180)

    # ef
    # ef = EfficientFrontier(mu, sigma)
    ret_ef = np.arange(0, max(mu), 0.001)
    vol_ef = []
    for i in np.arange(0, max(mu), 0.001):
        ef = EfficientFrontier(mu, sigma)
        ef.efficient_return(i)
        vol_ef.append(ef.portfolio_performance()[1])

    ef = EfficientFrontier(mu, sigma)
    ef.min_volatility()
    min_vol_ret = ef.portfolio_performance()[0]
    min_vol_vol = ef.portfolio_performance()[1]

    ef = EfficientFrontier(mu, sigma)
    ef.max_sharpe(risk_free_rate=0.04)
    max_sharpe_ret = ef.portfolio_performance()[0]
    max_sharpe_vol = ef.portfolio_performance()[1]
    # Create a figure with Plotly
    fig = go.Figure()
    # Adding the Efficient Frontier line plot
    fig.add_trace(go.Scatter(x=vol_ef, y=ret_ef, mode='lines',marker=dict(color='blue', size=5), name='Efficient Frontier'))
    # Adding scatter plot for Minimum Variance Portfolio
    fig.add_trace(go.Scatter(x=[min_vol_vol], y=[min_vol_ret], mode='markers', name='Minimum Variance Portfolio',
                            marker=dict(color='purple', size=10)))           
    # Adding scatter plot for Maximum Sharpe Portfolio
    fig.add_trace(go.Scatter(x=[max_sharpe_vol], y=[max_sharpe_ret], mode='markers', name='Maximum Sharpe Portfolio',
                            marker=dict(color='green', size=10)))
    # Adding the Capital Market Line
    x_points = [0, max_sharpe_vol]
    y_points = [0.04, max_sharpe_ret]
    # Calculate slope (m) and y-intercept (b)
    m = (y_points[1] - y_points[0]) / (x_points[1] - x_points[0])
    b = y_points[0] - m * x_points[0]
    # Define a range of x values for drawing the line
    extended_x = [min(x_points) - 1, max(x_points) + 1]  # Extend 1 unit beyond each side for demonstration
    extended_y = [m * x + b for x in extended_x]
    fig.add_trace(go.Scatter(x=extended_x, y=extended_y, mode='lines', name='Capital Market Line', line=dict(color='red')))
    # Update layout
    fig.update_layout(title='Efficient Frontier', title_x=0.5, title_font_size=20,
                    xaxis_title='Volatility', yaxis_title='Return',
                    xaxis=dict(range=[0, max(vol_ef)+0.1]), yaxis=dict(range=[0, max(mu)+0.5]),
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
            yaxis=dict(autorange="reversed"), # To invert the y-axis
            title="Your Chart Title",
            title_x=0.5
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
    raw_weights_maxsharpe_exp = ef.max_sharpe(risk_free_rate=0.04)
    draw_ticker_distribution(raw_weights_maxsharpe_exp)