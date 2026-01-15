import pandas as pd

def clean_amazon_sales_data(file_path):
    """
    Load and clean Amazon sales data.
    - Parses dates
    - Converts numeric fields
    - Removes invalid or cancelled orders
    - Adds default values for missing columns
    """
    df = pd.read_csv(file_path)

    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Convert numeric columns
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    # Handle missing 'Quantity' column
    if 'Quantity' not in df.columns:
        df['Quantity'] = 1
        print("INFO: 'Quantity' missing, setting default: 1")

    # Handle missing 'Fulfillment' column
    if 'Fulfillment' not in df.columns:
        df['Fulfillment'] = 'Unknown'
        print("INFO: 'Fulfillment' missing, setting default: Unknown")

    # Remove invalid rows
    before_rows = len(df)
    df = df.dropna(subset=['Date', 'Amount'])
    df = df[df['Quantity'] > 0]
    removed_rows = before_rows - len(df)

    print(f"Cleaning complete. Removed {removed_rows} invalid rows.")
    return df


def calculate_time_series_sales(df):
    """
    Returns daily and monthly total sales with renamed columns for visualization.
    """
    temp = df.set_index('Date')
    daily = temp['Amount'].resample('D').sum().reset_index()
    monthly = temp['Amount'].resample('ME').sum().reset_index()

    # Rename columns for consistency with visualization
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
        print("INFO: 'B2B' column missing, setting default: False for all rows.")

    return df.groupby('B2B').agg(
        Total_Sales=('Amount', 'sum'),
        Avg_Order_Value=('Amount', 'mean'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()
