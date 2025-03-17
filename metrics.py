METRICS = {
    "revenue_growth": {
        "name": "Revenue Growth",
        "description": "The percentage increase in revenue from the previous year.",
        "unit": "%",
        "format": "{:.1f}%",
        "formula": "income['Total Revenue'].pct_change(periods=-1) * 100",
    },
}


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
    