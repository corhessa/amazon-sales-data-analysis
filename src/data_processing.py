import pandas as pd

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Load and clean Amazon sales CSV.
    - Handles missing columns
    - Converts types
    - Assigns defaults for missing critical columns
    """
    df = pd.read_csv(file_path, low_memory=False)

    # Column mapping for different CSV variants
    column_mapping = {
        'Delivery Method': 'Fulfillment',
        'Order Amount': 'Amount',
        'Client Type': 'B2B'
    }
    df.rename(columns=column_mapping, inplace=True)

    # Ensure critical columns exist
    defaults = {
        'Quantity': 1,
        'Fulfillment': 'Unknown',
        'B2B': False
    }

    for col, default in defaults.items():
        if col not in df.columns:
            print(f"INFO: '{col}' missing, setting default: {default}")
            df[col] = default

    # Parse dates and numeric fields
    if 'Date' not in df.columns:
        raise ValueError("CRITICAL: 'Date' column is missing.")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1)

    # Drop invalid rows
    before = len(df)
    df = df.dropna(subset=['Date', 'Amount'])
    df = df[df['Quantity'] > 0]
    removed = before - len(df)
    print(f"Cleaning complete. Removed {removed} invalid rows.")

    return df
