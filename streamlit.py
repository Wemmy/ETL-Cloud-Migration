import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def fetch_and_plot_technical_data(ticker, timeframe):
    api_key = os.getenv('API_KEY')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * timeframe)  # Adjust the number of days as needed for the timeframe
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start_date_str}&to={end_date_str}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and 'historical' in data:
            df = pd.DataFrame(data['historical'])
            df['date'] = pd.to_datetime(df['date'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name='Close Price'))
            st.plotly_chart(fig)
        else:
            st.error(f"No historical data available for {ticker}.")
    else:
        st.error(f"Failed to fetch historical data for {ticker}. Status code: {response.status_code}")

def fetch_company_data(ticker):
    api_key = os.getenv('API_KEY')
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        st.error(f"Failed to fetch data for {ticker}. Status code: {response.status_code}")
        return None

def fetch_ratios_ttm(ticker):
    api_key = os.getenv('API_KEY')
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        st.error(f"Failed to fetch TTM ratios for {ticker}. Status code: {response.status_code}")
        return None

def fetch_company_rating(ticker):
    api_key = os.getenv('API_KEY')
    url = f"https://financialmodelingprep.com/api/v3/rating/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        st.error(f"Failed to fetch rating data for {ticker}. Status code: {response.status_code}")
        return None

def fetch_time_return(ticker):
    api_key = os.getenv('API_KEY')
    url = f"https://financialmodelingprep.com/api/v3/stock-price-change/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        st.error(f"Failed to fetch rating data for {ticker}. Status code: {response.status_code}")
        return None

def main():
    st.title("Company Information and Historical Prices")

    ticker = st.sidebar.text_input("Enter a stock symbol:")
    
    timeframe_options = {
        '5 Years': 5,
        '1 Year': 1,
        '3 Months': 0.25,
        '1 Month': 1/12,
        '1 Week': 1/52
    }

    timeframe = st.selectbox("Select timeframe:", list(timeframe_options.keys()))


    if ticker:
        st.write(f"Displaying historical prices for {ticker}")
        company_data = fetch_company_data(ticker)
        if company_data is not None:
            st.sidebar.write("**Company Information**")
            st.sidebar.write("Company Name:", company_data.get('name', 'Not available'))
            st.sidebar.write("Symbol:", company_data.get('symbol', 'Not available'))
            st.sidebar.write("Price:", company_data.get('price', 'Not available'))
            st.sidebar.write("Previous Closing Price:", company_data.get('previousClose', 'Not available'))
            st.sidebar.write("% Change:", company_data.get('changesPercentage', 'Not available'))
            st.sidebar.write("Change:", company_data.get('change', 'Not available'))
            st.sidebar.write("Year Low:", company_data.get('yearLow', 'Not available'))
            st.sidebar.write("Year High:", company_data.get('yearHigh', 'Not available'))
            st.sidebar.write("50 Days Average Price:", round(company_data.get("priceAvg50", 'Not available'),2))
            st.sidebar.write("200 Days Average Price:", round(company_data.get("priceAvg200", 'Not available'), 2))
            st.sidebar.write("Day Low:", company_data.get('dayLow', 'Not available'))
            st.sidebar.write("Day High:", company_data.get('dayHigh', 'Not available'))
            st.sidebar.write("Volume Average:", company_data.get('avgVolume', 'Not available'))
            st.sidebar.write("EPS:", company_data.get('eps', 'Not available'))
            st.sidebar.write("P/E Ratio:", company_data.get('pe', 'Not available'))
            st.sidebar.write("Market Cap:", company_data.get('marketCap', 'Not available'))
            
            # Fetch and plot historical data
            fetch_and_plot_technical_data(ticker, timeframe_options[timeframe])
            
            # Fetch and display Stock Price Change
            show_change = st.sidebar.checkbox('Show Stock Price Change Through Time')
            if show_change:
                change_ratio = fetch_time_return(ticker)
                if change_ratio:
                    st.write("Stock Price Change(%)")
                    st.write("1 Day:", change_ratio.get("1D"))
                    st.write("5 Days:", change_ratio.get("5D"))
                    st.write("1 Month:", change_ratio.get("1M"))
                    st.write("3 Months:", change_ratio.get("3M"))
                    st.write("6 Months:", change_ratio.get("6M"))
                    st.write("Year to Date:", change_ratio.get("ytd"))
                    st.write("1 Year:", change_ratio.get("1Y"))
                    st.write("3 Years:", change_ratio.get("3Y"))
                    st.write("5 Years:", change_ratio.get("5Y"))

            # Fetch and display liquidity ratios
            show_liquidity_ratios = st.button("Show Liquidity Ratios")
            if show_liquidity_ratios:
            # Fetch and display liquidity ratios
                liquidity_ratios = fetch_ratios_ttm(ticker)
                if liquidity_ratios is not None:
                    liquidity_ratios_data = {
                        'Current Ratio': liquidity_ratios.get('currentRatioTTM'),
                        'Quick Ratio': liquidity_ratios.get('quickRatioTTM'),
                        'Cash Ratio': liquidity_ratios.get('cashRatioTTM')
                    }
                    liquidity_ratios_df = pd.DataFrame.from_dict(liquidity_ratios_data, orient='index', columns=['Value'])
                    st.subheader("Liquidity Ratios (12 Months trailing)")
                    st.bar_chart(liquidity_ratios_df)
                else:
                    st.error(f"No liquidity ratios data available for {ticker}.")

                
            # Fetch and display solvency ratios
            show_solvency_ratios = st.button("Show Solvency Ratios")
            if show_solvency_ratios:
                solvency_ratios = fetch_ratios_ttm(ticker)
                if solvency_ratios is not None:
                    solvency_ratios_data = {
                        'Debt Ratio': solvency_ratios.get('debtRatioTTM'),
                        'Debt/Equity Ratio': solvency_ratios.get('debtEquityRatioTTM'),
                        'Long Term Debt to Capitalization': solvency_ratios.get('longTermDebtToCapitalizationTTM'),
                        'Total Debt to Capitalization': solvency_ratios.get('totalDebtToCapitalizationTTM')
                    }
                    solvency_ratios_df = pd.DataFrame.from_dict(solvency_ratios_data, orient='index', columns=['Value'])
                    st.subheader("Solvency Ratios (12 Months trailing)")
                    st.bar_chart(solvency_ratios_df)
                else:
                    st.error(f"No solvency ratios data available for {ticker}.")
            
            # Fetch and display company rating
            company_rating = st.sidebar.checkbox("Show Company Ratings")
            if company_rating:
                ccompany_rating = fetch_company_rating(ticker)
                if ccompany_rating is not None:
                    st.title("Company Rating")
                    st.write("Rating:", ccompany_rating.get('rating', 'Not available'))
                    st.write("Rating Score:", ccompany_rating.get('ratingScore', 'Not available'))
                    st.write("Rating Recommendation:", ccompany_rating.get('ratingRecommendation', 'Not available'))
                    st.write("**Rating Details**")
                    st.write("DCF Score:", ccompany_rating.get('ratingDetailsDCFScore', 'Not available'))
                    st.write("DCF Recommendation:", ccompany_rating.get('ratingDetailsDCFRecommendation', 'Not available'))
                    st.write("ROE Score:", ccompany_rating.get('ratingDetailsROEScore', 'Not available'))
                    st.write("ROE Recommendation:", ccompany_rating.get('ratingDetailsROERecommendation', 'Not available'))
                    st.write("ROA Score:", ccompany_rating.get('ratingDetailsROAScore', 'Not available'))
                    st.write("ROA Recommendation:", ccompany_rating.get('ratingDetailsROARecommendation', 'Not available'))
                    st.write("DE Score:", ccompany_rating.get('ratingDetailsDEScore', 'Not available'))
                    st.write("DE Recommendation:", ccompany_rating.get('ratingDetailsDERecommendation', 'Not available'))
                    st.write("PE Score:", ccompany_rating.get('ratingDetailsPEScore', 'Not available'))
                    st.write("PE Recommendation:", ccompany_rating.get('ratingDetailsPERecommendation', 'Not available'))
                    st.write("PB Score:", ccompany_rating.get('ratingDetailsPBScore', 'Not available'))
                    st.write("PB Recommendation:", ccompany_rating.get('ratingDetailsPBRecommendation', 'Not available'))
                else:
                    st.error(f"No rating data available for {ticker}.")


if __name__ == "__main__":
    main()
