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

@st.cache_data
def get_balance_sheet(ticker: str):
    """
    Fetches the balance sheet data from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing balance sheet data.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.balance_sheet.T
    except Exception as e:
        st.error(f"Error fetching balance sheet data for ticker {ticker}: {e}")
        return pd.DataFrame()

@st.cache_data
def get_income_statement(ticker: str):
    """
    Fetches the income statement data from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing income statement data.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.financials.T
    except Exception as e:
        st.error(f"Error fetching income statement data for ticker {ticker}: {e}")
        return pd.DataFrame()    

@st.cache_data
def get_cash_flow(ticker: str):
    """
    Fetches the cash flow data from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing cash flow data.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.cashflow.T
    except Exception as e:
        st.error(f"Error fetching cash flow data for ticker {ticker}: {e}")
        return pd.DataFrame()   

@st.cache_data
def get_financials(ticker: str):
    """
    Fetches the financial data from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing financial data.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.financials.T
    except Exception as e:
        st.error(f"Error fetching financial data for ticker {ticker}: {e}")
        return pd.DataFrame() 

@st.cache_data
def get_all(ticker: str):
    """
    Fetches all available financial statements from Yahoo Finance: balance, sheet, income statement, cash flow, and financials.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    dict: A dictionary containing all available data.
    """
    try:
        bs = get_balance_sheet(ticker)
        is_ = get_income_statement(ticker)
        cf = get_cash_flow(ticker)
        fin = get_financials(ticker)
        return {"balance": bs, "income": is_, "cashflow": cf, "financials": fin}
    except Exception as e:
        st.error(f"Error fetching all data for ticker {ticker}: {e}")
        return {}  