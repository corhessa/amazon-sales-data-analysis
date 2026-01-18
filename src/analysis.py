import pandas as pd


def calculate_time_series_sales(df):
    """
    Returns daily and monthly total sales with renamed columns for visualization.
    """
    temp = df.set_index('Date')

    daily = temp['Amount'].resample('D').sum().reset_index()
    monthly = temp['Amount'].resample('ME').sum().reset_index()

    daily.rename(columns={'Amount': 'Daily_Total'}, inplace=True)
    monthly.rename(columns={'Amount': 'Monthly_Total'}, inplace=True)

    return daily, monthly


def compare_fulfillment_methods(df):
    """
    Compares total sales and order count by fulfillment type.
    """
    return df.groupby('Fulfillment').agg(
        Total_Sales=('Amount', 'sum'),
        Order_Count=('Amount', 'count')
    ).reset_index()


def compare_business_segments(df):
    """
    Compares B2B and B2C customer segments.
    """
    if 'B2B' not in df.columns:
        df['B2B'] = False

    return df.groupby('B2B').agg(
        Total_Sales=('Amount', 'sum'),
        Avg_Order_Value=('Amount', 'mean'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()
