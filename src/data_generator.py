import pandas as pd
import random
from datetime import datetime, timedelta

def generate_dummy_data(rows=1500):
    """Generates a DataFrame with dummy e-commerce data"""
    regions = ['North', 'South', 'East', 'West']
    categories = ['Furniture', 'Office Supplies', 'Technology']
    
    data = []
    # Generate data for the last 365 days
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(rows):
        order_id = f"ORD-{1000+i}"
        date = start_date + timedelta(days=random.randint(0, 365))
        customer_id = f"CUST-{random.randint(1, 100)}" # 100 Unique customers
        region = random.choice(regions)
        category = random.choice(categories)
        sales = round(random.uniform(20, 1500), 2)
        # Profit margin varies by category
        if category == 'Furniture':
            profit = round(sales * random.uniform(-0.1, 0.3), 2) # Higher risk of loss
        else:
            profit = round(sales * random.uniform(0.1, 0.5), 2) 
        
        data.append([order_id, date, customer_id, region, category, sales, profit])
        
    df = pd.DataFrame(data, columns=['Order ID', 'Order Date', 'Customer ID', 'Region', 'Category', 'Sales', 'Profit'])
    return df
