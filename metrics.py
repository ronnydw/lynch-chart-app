# Description: This file contains the metric definitions and functions to fetch metric data.
#
# The METRICS dictionary contains the metric definitions, including the formula to calculate the metric.
# The get_3y_metric function fetches the 3-year metric data from Yahoo Finance using the stock data.    

import pandas as pd
import streamlit as st
import json

# Load the METRICS dictionary from the JSON file
with open('metrics.json', 'r') as f:
    METRICS = json.load(f)

def get_3y_metric(stock_data: dict, metric: str):
    """
    Fetches the 3-year metric data from Yahoo Finance.

    Parameters:
    metric (str): The metric to fetch.

    Returns:
    pd.DataFrame: A DataFrame containing 3-year metric data for a stock, 
    including evolution and average values.
    """
    # get metric defintion
    metric_def = METRICS[metric]
    if not metric_def:
        st.error(f"Error fetching metric data for {metric}: Metric not found.")
        return pd.DataFrame()

    # get stock data
    income, balance, cashflow = stock_data['income'], stock_data['balance'], stock_data['cashflow']
    if income.empty or balance.empty or cashflow.empty:
        st.error(f"Error fetching metric data for {metric}: Stock data not found.")
        return pd.DataFrame()

    # get metric data
    try:
        metric_data = eval(metric_def['formula'])
        return metric_data
    except Exception as e:
        st.error(f"Error fetching metric data for {metric}: {e}")
        return pd.DataFrame()
    