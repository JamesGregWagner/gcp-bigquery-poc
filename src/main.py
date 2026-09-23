from data_quality import run_raw_quality_checks
from transform import transform_orders, run_staging_quality_checks
import pandas as pd
from load_bigquery import load_dataframe_to_bigquery

## Load the raw data
df = pd.read_csv('data/orders.csv')

#Quality checks and generate a report
raw_quality_report = run_raw_quality_checks(df)
raw_quality_report_df = pd.DataFrame([raw_quality_report])

#Transform the data and generate a report
df_transformed, duplicates_lines_dropped, missing_values_dropped = transform_orders(df)
staging_quality_report = run_staging_quality_checks(df_transformed, duplicates_lines_dropped, missing_values_dropped)
staging_quality_report_df = pd.DataFrame([staging_quality_report])

# Add STAGING report
quality_report_df = pd.concat([raw_quality_report_df, staging_quality_report_df],ignore_index=True)

# Save RAW + STAGING reports
quality_report_df.to_csv('data/data_quality_report.csv',index=False)

# Store data into BigQuery
load_dataframe_to_bigquery(
    df=df_transformed,
    project_id="portofolio-bigquery-demo",
    dataset_id="sales_analytics",
    table_id="orders_staging"
)
