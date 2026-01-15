import matplotlib.pyplot as plt
import pandas as pd

def plot_daily_sales_trend(daily_df: pd.DataFrame):
    """Plots daily sales trend with formatted y-axis."""
    plt.figure()
    plt.plot(daily_df['Date'], daily_df['Daily_Total'], color='#1f77b4',
             linewidth=2, marker='o', markersize=4)
    plt.title('Daily Sales Trend', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().get_yaxis().set_major_formatter(
        plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
    )
    plt.tight_layout()
    plt.savefig('daily_sales_trend.png')
    plt.clf()


def plot_fulfillment_comparison(fulfillment_df: pd.DataFrame):
    """Plots FBA vs Merchant sales comparison, normalizing unknowns."""
    df_sorted = fulfillment_df.copy()

    # Normalize empty or missing fulfillment values
    df_sorted['Fulfillment'] = df_sorted['Fulfillment'].fillna('Unknown')
    df_sorted['Fulfillment'] = df_sorted['Fulfillment'].replace('', 'Unknown')

    df_sorted = df_sorted.sort_values(by='Total_Sales', ascending=False)
    colors = ['#ff9933' if x != 'Unknown' else '#cccccc' for x in df_sorted['Fulfillment']]

    plt.figure()
    plt.bar(df_sorted['Fulfillment'], df_sorted['Total_Sales'], color=colors)
    plt.title('Fulfillment Comparison: Total Sales', fontsize=14)
    plt.xlabel('Fulfillment Method')
    plt.ylabel('Total Sales ($)')
    plt.gca().get_yaxis().set_major_formatter(
        plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
    )
    plt.tight_layout()
    plt.savefig('fulfillment_comparison.png')
    plt.clf()


def plot_business_segment_comparison(segment_df: pd.DataFrame):
    """Plots B2B vs B2C sales comparison."""
    df_plot = segment_df.copy()
    df_plot['Label'] = df_plot['B2B'].map({True: 'B2B', False: 'B2C'})
    df_plot = df_plot.sort_values(by='Total_Sales', ascending=False)

    plt.figure()
    plt.bar(df_plot['Label'], df_plot['Total_Sales'], color=['#9467bd', '#8c564b'])
    plt.title('B2B vs B2C: Total Sales', fontsize=14)
    plt.xlabel('Customer Segment')
    plt.ylabel('Total Sales ($)')
    plt.gca().get_yaxis().set_major_formatter(
        plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
    )
    plt.tight_layout()
    plt.savefig('business_segment_comparison.png')
    plt.clf()
