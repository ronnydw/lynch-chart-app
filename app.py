import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import yfinance as yf
import matplotlib.ticker as mticker
from datetime import timedelta

def plot_lynch_style_chart(df: pd.DataFrame, company: str):
    """
    Plots a 20-year historical price chart with monthly high-lows and a logarithmic y-axis,
    similar to charts from Peter Lynch's books.

    Parameters:
    df (pd.DataFrame): A DataFrame with columns 'Date', 'High', and 'Low'.
    company (str): The name of the stock company.
    """

    # Sort data by date
    df = df.sort_values('Date')

    # Ensure 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    ticker = df.columns[1][1]

    # Set start and end dates
    start_date = pd.Timestamp.today().replace(year=pd.Timestamp.today().year - 20, month=1, day=1)
    end_date = pd.Timestamp.today().replace(year=pd.Timestamp.today().year + 1, month=1, day=1)
    
    # Set figure size and style
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_yscale("log")  # Logarithmic y-axis
    ax.set_title(company + " 20-Year Price History" , fontsize=14, fontweight='bold')
    
    # Plot high-low bars for each month
    ax.vlines(df['Date'], df['Low'], df['High'], color='grey', linewidth=2)
    
    # Formatting x-axis to show years and quarters with boundary tick lines
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))  # Every quarter

    # Adjust y-axis limits based on data range
    low_min = df['Low', ticker].min() * 0.9
    high_max = df['High', ticker].max() * 1.1
    ax.set_ylim(low_min, high_max)
    
    # Draw yearly boxes and year labels centered in each box
    years = pd.date_range(start=start_date, end=end_date, freq='YS-JAN')
    for year in years[:-1]:
        ax.axvline(year, color='gray', linestyle='-', linewidth=0.6)
        ax.text((year + pd.DateOffset(months=6)), low_min * 0.95, year.strftime('%y'), 
                ha='center', va='top', fontsize=10)    

    # Draw Copyright
    ax.text(end_date + timedelta(days=-100), low_min * 1.1, "(C) Ronny De Winter", 
            ha='right', va='bottom', fontsize=8, color='grey', backgroundcolor='white')    
    
    # Draw major tick lines for year boundaries
    for year in pd.date_range(start_date, end_date, freq='YS-JAN'):
        ax.axvline(year, color='gray', linestyle='-', linewidth=0.6)
    
    # Ensure quarter tick lines align with year lines
    ax.grid(True, which='major', linestyle='solid', linewidth=0.6)
    ax.grid(True, which='minor', linestyle='dashed', linewidth=0.3)

    # Set y-axis to use decimal notation and add labels on every tick
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.2f}'))
    ax.yaxis.set_minor_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.2f}'))
    for label in ax.get_yticklabels() + ax.get_yticklabels(minor=True):
        label.set_fontsize(8)  # Reduce font size to avoid overlap
    
    # Remove x-axis labels and ticks
    ax.set_xticklabels([])
    ax.set_xticks([])
    
    # Y label
    ax.set_ylabel("Price (Log Scale)", fontsize=10)
    
    ax.margins(x=0)
    # fig.savefig('./img/'+ ticker + '-20y-history.jpg', format='jpg')

    return fig

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
        return df
    except Exception as e:
        st.error(f"Error fetching data for ticker {ticker}: {e}")
        return pd.DataFrame()

@st.cache_data
def get_company_name(ticker: str):
    """
    Fetches the company name from Yahoo Finance.

    Parameters:
    ticker (str): The Yahoo Finance ticker symbol.

    Returns:
    The full name of the company 
    """    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info.get('longName', 'Unknown Company')
    except Exception as e:
        st.error(f"Error fetching company name for ticker {ticker}: {e}")
        return 'Unknown Company'

st.title("The Only Price Chart a Quality Investor Needs")
ticker = st.text_input("Enter a yahoo stock ticker symbol:", "AAPL")
if st.button("Generate Chart"):
    df = get_yahoo_historical_data(ticker)
    if not df.empty:
        company = get_company_name(ticker)
        fig = plot_lynch_style_chart(df, company)
        st.pyplot(fig)
    else:
        st.error("Please enter a valid ticker symbol. You can find ticker symbols on Yahoo Finance: https://finance.yahoo.com/ .")