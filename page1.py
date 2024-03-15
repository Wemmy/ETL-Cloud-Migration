import streamlit as st

import pandas as pd
from plotly import graph_objs as go
from datetime import datetime,timedelta
import yfinance as yf
import os
from dotenv import load_dotenv
load_dotenv()
from local_deployment.utils.PostgreDB.db_connect import create_connection
from local_deployment.utils.utils import show_news
from local_deployment.utils.dynamodb.db_connect import get_topic_data_sorted, get_data_from_dynamodb


def app():

    # # Layout
    st.title("Market Overview")
    # Function to fetch data
    @st.cache_data
    def get_data(ticker, start, end):
        return yf.download(ticker, start, end)

    # Mapping user selection to ticker symbols
    index_symbols = {
        "S&P 500": "^GSPC",
        "Dow 30": "^DJI",
        "NASDAQ Composite": "^IXIC",
        "Russell 2000": "^RUT",
        "NYSE COMPOSITE":"^NYA"
    }

    # Time frame selection
    time_frames = {
        # "1D": 1,
        # "5D": 5,
        "1M": 30,
        "6M": 182,
        "1Y": 365,
        "5Y": 5*365,
        "6Y": 6*365
    }

    col1, col2 = st.columns(2)
    with col1:
        # Sidebar for navigation or filtering (example)
        selected_index = st.radio("Indices", list(index_symbols.keys()), horizontal=True)

    with col2:
        # Buttons for time frame selection
        selected_time_frame = st.radio("Time Frame", list(time_frames.keys()), horizontal= True)

    # Calculate start date based on selected time frame
    end_date = datetime.today()
    start_date = end_date - timedelta(days=time_frames[selected_time_frame])

    # Fetching data
    data = get_data(index_symbols[selected_index], start_date, end_date)
    # Plotting
    fig = go.Figure(data=go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(color='blue', shape='spline', smoothing=1.3)))
    st.plotly_chart(fig, use_container_width=True)

    # connection config
    DB_ENDPOINT = os.environ.get('RDS_ENDPOINT')
    DB_USER = os.environ.get('RDS_USER')
    DB_PASSWORD = os.environ.get('RDS_PASSWORD')
    DB_PORT = os.environ.get('RDS_PORT')
    DB_NAME = os.environ.get('RDS_DBNAME')

    # start creating eco metrics
    psql_conn = create_connection(DB_ENDPOINT, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME)

    @st.cache_resource
    def query_data(indicator):
        query = f"SELECT * FROM dashboard_raw.{indicator}"
        df = pd.read_sql(query, psql_conn)
        return df

    # Economic indicators available for selection
    indicators = ['gdp', 'cpi', 'durables', 'fed_fund_rate', 'gdp_per_capita',
                'inflation', 'nonfarm-payroll', 'retail_sales', 'treasury_yield', 'unemployment']

    indicator_units = {
        'gdp':'billions of dollars', 
        'cpi':'index', 
        'durables':'millions of dollars', 
        'fed_fund_rate':'percent', 
        'gdp_per_capita':'chained 2012 dollars',
        'inflation':'percent', 
        'nonfarm-payroll':'thousands of persons', 
        'retail_sales':'millions of dollars', 
        'treasury_yield':'percent', 
        'unemployment':'percent'}

    # User selection of indicators
    selected_indicators = st.multiselect('Select up to two Economic Indicators', indicators, 'fed_fund_rate')

    # Limit the selection to a maximum of 2
    if len(selected_indicators) > 2:
        st.warning('Please select no more than two indicators.')
        selected_indicators = selected_indicators[:2]

    # Fetch and store data for selected indicators
    indicator_data = {}
    for indicator in selected_indicators:
        indicator_data[indicator] = query_data(indicator)

    # Determine the shortest time range
    min_date = pd.Timestamp('1900-01-01')  # Initial high value
    max_date = pd.Timestamp('2099-12-31')  # Initial low value

    for data in indicator_data.values():
        # Ensure data['date'] is in datetime format
        data['date'] = pd.to_datetime(data['date'])
        min_date = max(min_date, data['date'].min())
        max_date = min(max_date, data['date'].max())

    # Create a figure with secondary y-axis
    fig = go.Figure()

    # Add traces for the selected indicators
    for i, indicator in enumerate(selected_indicators):
        unit = indicator_units.get(indicator, '')
        data = indicator_data[indicator]
        axis_title = f"{indicator} ({unit})"
        if i == 0:  # First selected indicator uses the left y-axis
            fig.add_trace(go.Scatter(x=data['date'], y=data['value'], mode='lines', name=indicator, line=dict( shape='spline', smoothing=1.3)))
            fig.update_layout(yaxis=dict(title=axis_title))
        elif i == 1:  # Second selected indicator uses the right y-axis
            fig.add_trace(go.Scatter(x=data['date'], y=data['value'], mode='lines', name=indicator, line=dict(shape='spline', smoothing=1.3), yaxis='y2'))
            fig.update_layout(yaxis2=dict(title=axis_title, overlaying='y', side='right'))

    # Update layout for secondary y-axis
    fig.update_layout(
        xaxis=dict(
            range=[min_date, max_date]  # Set the range for x-axis
        )
    )
    # Show the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)


    table_name = 'dashboard_news'
    items, topics = get_data_from_dynamodb(table_name)
    st.header("News")
    # Dropdown menu for topic selection
    selected_topic = st.selectbox("Choose a News Topic", topics, index=0)
    news = get_topic_data_sorted(items,selected_topic)

    # Slice to get [1, 3, 5] and [2, 4, 6]
    news_odd = [news[i] for i in range(10) if i % 2 == 0]
    news_even = [news[i] for i in range(10) if i % 2 != 0]

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        show_news(news_odd)
    with col2:
        show_news(news_even)