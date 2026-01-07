import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# Create data folder if not exists
if not os.path.exists('data'):
    os.makedirs('data')

def generate_dummy_data(rows=1000):
    print("Generating dummy data...")
    
    regions = ['North', 'South', 'East', 'West']
    categories = ['Furniture', 'Office Supplies', 'Technology']
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    data = []
    
    for i in range(rows):
        order_id = f"ORD-{1000+i}"
        date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        customer_id = f"CUST-{random.randint(1, 100)}" # 100 Unique customers
        region = random.choice(regions)
        category = random.choice(categories)
        sales = round(random.uniform(10, 1000), 2)
        # Profit is usually -20% to +40% of sales
        profit = round(sales * random.uniform(-0.2, 0.4), 2) 
        
        data.append([order_id, date, customer_id, region, category, sales, profit])
        
    df = pd.DataFrame(data, columns=['Order ID', 'Order Date', 'Customer ID', 'Region', 'Category', 'Sales', 'Profit'])
    
    # Save to CSV
    df.to_csv('data/superstore.csv', index=False)
    print("✅ data/superstore.csv created successfully!")

if __name__ == "__main__":
    generate_dummy_data()
