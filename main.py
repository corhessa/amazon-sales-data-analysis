import os
import sys
from src.data_processing import load_and_clean_data
from src.analysis import calculate_time_series_sales, compare_fulfillment_methods, compare_business_segments
from src.visualization import plot_daily_sales_trend, plot_fulfillment_comparison, plot_business_segment_comparison

def main():
    data_path = os.path.join("data", "Amazon Sale Report.csv")
    if not os.path.exists(data_path):
        sys.exit("ERROR: CSV not found")

    df = load_and_clean_data(data_path)

    if df.empty:
        sys.exit("ERROR: No valid data to analyze")

    daily_sales, monthly_sales = calculate_time_series_sales(df)
    fulfillment_summary = compare_fulfillment_methods(df)
    segment_summary = compare_business_segments(df)

    # Save visualizations
    plot_daily_sales_trend(daily_sales)
    plot_fulfillment_comparison(fulfillment_summary)
    plot_business_segment_comparison(segment_summary)

if __name__ == "__main__":
    main()
