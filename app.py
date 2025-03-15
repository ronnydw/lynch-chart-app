import streamlit as st
from data import get_yahoo_historical_data, get_company_name
from plot import plot_lynch_style_chart

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
        