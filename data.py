import pandas as pd
import yfinance as yf
import streamlit as st

@st.cache_data
def get_yahoo_historical_data(ticker: str):
    """
    Fetches historical monthly price data for the past 20 years from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing 'Date', 'High', and 'Low' columns.
    """
    try:
        end_date = pd.to_datetime("today")
        start_date = end_date - pd.DateOffset(years=20)       
        data = yf.download(ticker, start=start_date, end=end_date, interval="1mo")
        df = data[['High', 'Low']].reset_index()
        df.columns = ['Date', 'High', 'Low']  # Rename columns to remove ticker symbol
        return df
    except Exception as e:
        st.error(f"Error fetching data for ticker {ticker}: {e}")
        return pd.DataFrame()

@st.cache_data
def get_company_info(ticker: str):
    """
    Fetches company information from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    dict: A dictionary containing company information.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception as e:
        st.error(f"Error fetching company information for ticker {ticker}: {e}")
        return {}        
