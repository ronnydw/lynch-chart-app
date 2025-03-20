# caluculate the score of the model, based on the scoring parameters defined in the config file *_score.json

import json
import pandas as pd
import metrics

def get_score_definitions(file_path = "default_score.json"):
    """
    Loads the scoring parameters from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file containing scoring parameters.

    Returns:
    dict: A dictionary containing scoring parameters.
    """
    with open(file_path, 'r') as f:
        return json.load(f) 

def calculate_metric_score(metric: str, parms: dict, data: dict):
    """
    Calculates the score of a metric based on the scoring parameters defined in the config file *_score.json.

    Parameters:
    metric (str): The metric identifier.
    score_params (dict): The scoring parameters.
    data (dict): A dictionary containing the reporting data for the stock: balance, income, cashflow and financial statements.

    Returns:
    scores (dict): The scores of the metric per type of score. Possible types are "yearly", "latest", "average", "cagr".
    """
    MONTH = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

    OPERATOR = {"greater_than": ">", "less_than": "<", "equal_to": "=="}

    metric_history = metrics.get_3y_metric(data, metric)

    if metric_history.empty:
        return {}

    fiscal_year_end = MONTH[metric_history.index[0].month]
    years = metric_history.index.year
    metric_history.index = pd.to_datetime(metric_history.index).year

    scores = []

    multiplier = parms["score"] * parms["weight"]
    for score_type in parms["type"]:
        if score_type == "yearly":
            formula = f"metric_history {OPERATOR[parms["operator"]]} {parms["value"]}"
            score_df = eval(formula).astype(int) * multiplier
            for year in years:
                scores.append({
                    "Metric": metric,
                    "Type": f"y_{year}",
                    "Value": metric_history.loc[year],
                    "Score": score_df.loc[year]
                })
        elif score_type == "latest":
            formula = f"metric_history.iloc[0] {OPERATOR[parms["operator"]]} {parms["value"]}"
            score = int(eval(formula)) * parms["score"] * parms["weight"]
            scores.append({
                "Metric": metric,
                "Type": f"y_{years[0]}",
                "Value": metric_history.iloc[0],
                "Score": score
            })
        elif score_type == "average":
            formula = f"metric_history.mean() {OPERATOR[parms["operator"]]} {parms["value"]}"
            score = int(eval(formula)) * parms["score"] * parms["weight"]
            scores.append({
                "Metric": metric,
                "Type": score_type,
                "Value": metric_history.mean(),
                "Score": score
            })            
        elif score_type == "cagr":
            years = metric_history.shape[0]
            cagr = ((metric_history.iloc[-1] / metric_history.iloc[0]) ** (1/years)) - 1
            formula = f"cagr {OPERATOR[parms["operator"]]} {parms["value"]}"
            score = int(eval(formula)) * parms["score"] * parms["weight"]
            scores.append({
                "Metric": metric,
                "Type": score_type,
                "Value": cagr,
                "Score": score
            })
        else:
            scores[score_type] = 0

    return pd.DataFrame(scores)

def get_score_table(data: dict, score_parameters: dict):
    """
    Calculates the score of the model based on the scoring parameters defined in the config file *_score.json.

    Parameters:
    data (dict): A dictionary containing the reporting data for the stock: balance, income, cashflow and financial statements.
    metrics (dict): A dictionary containing metric defintions.
    score_parameters (dict): A dictionary containing scoring parameters.

    Returns:
    DataFrame: The score table of the model.
    """
    score_table = pd.DataFrame()
    for metric in score_parameters.keys():
        score = calculate_metric_score(metric, score_parameters[metric], data)
        score_table = pd.concat([score_table, score], ignore_index=True)

    return score_table
