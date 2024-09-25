import pandas as pd
import json

df = pd.read_csv('arcade_orders.csv')

def analyze_csv(df):
    item_quantity = df.groupby('Full Name (from Item)')['Quantity'].sum().to_dict()
    total_order_price = int(df['Order Price (Minutes)'].sum())
    total_order_hours = total_order_price / 60
    country_orders = df.groupby('Address: Country')['Quantity'].sum().to_dict()
    most_popular_item = max(item_quantity, key=item_quantity.get)
    least_popular_item = min(item_quantity, key=item_quantity.get)
    top_5_items = dict(sorted(item_quantity.items(), key=lambda x: x[1], reverse=True)[:5])
    total_revenue = total_order_price
    avg_order_price = df['Order Price (Minutes)'].mean()
    most_expensive_item = df.loc[df['Frozen Unit Price (Minutes)'].idxmax()]['Full Name (from Item)']
    least_expensive_item = df.loc[df['Frozen Unit Price (Minutes)'].idxmin()]['Full Name (from Item)']
    multiple_item_orders = df[df['Quantity'] > 1]['Full Name (from Item)'].unique().tolist()
    country_percentage = (df['Address: Country'].value_counts() / len(df) * 100).to_dict()

    # Convert all int64 to int
    item_quantity = {k: int(v) for k, v in item_quantity.items()}
    country_orders = {k: int(v) for k, v in country_orders.items()}
    country_percentage = {k: float(v) for k, v in country_percentage.items()}

    analysis = {
        'total_quantity_per_item': item_quantity,
        'total_order_price_minutes': total_order_price,
        'total_order_price_hours': total_order_hours,
        'orders_per_country': country_orders,
        'most_popular_item': most_popular_item,
        'least_popular_item': least_popular_item,
        'top_5_items_by_quantity': top_5_items,
        'total_revenue': total_revenue,
        'avg_order_price': avg_order_price,
        'most_expensive_item': most_expensive_item,
        'least_expensive_item': least_expensive_item,
        'items_ordered_multiple_times': multiple_item_orders,
        'country_percentage': country_percentage
    }

    return analysis

analysis_results = analyze_csv(df)

output_file = 'analysis_results.json'
