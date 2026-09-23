import pandas as pd

df = pd.read_csv('data/orders.csv')

def run_raw_quality_checks(df):

    report = {}

    # Construire le rapport de qualité des données pour la couche RAW
    report["rows"] = len(df)
    report["layer"] = "RAW"
    report["columns"] = len(df.columns)
    report["duplicates"] = int(df.duplicated().sum())
    report["missing_values"] = int(df.isnull().any(axis=1).sum())
    report["invalid_prices"] = int((df["unit_price"] < 0).sum())
    report["invalid_quantities"] = int((df["quantity"] <= 0).sum())
    report["invalid_dates"] = int(df["order_date"].isnull().sum())
    report["duplicates_lines_dropped"] = 0
    report["missing_values_dropped"] = 0

    return report

