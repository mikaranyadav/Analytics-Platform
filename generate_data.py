import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# --- 1. Create Products Data ---
print("Generating products...")
product_list = []
for i in range(1, 101):  # 100 products
    product_list.append({
        'product_id': f'P{i:03d}',
        'product_name': f'Part {fake.word().capitalize()}-{i}',
        'category': random.choice(['Engine', 'Chassis', 'Interior', 'Electronics']),
        'unit_price': round(random.uniform(50, 5000), 2)
    })
products_df = pd.DataFrame(product_list)
products_df.to_csv('products.csv', index=False)

# --- 2. Create Customers Data ---
print("Generating customers...")
customer_list = []
for i in range(1, 51):  # 50 customers
    customer_list.append({
        'customer_id': f'C{i:03d}',
        'customer_name': fake.company(),
        'country': fake.country()
    })
customers_df = pd.DataFrame(customer_list)
customers_df.to_csv('customers.csv', index=False)

# --- 3. Create Quarterly Sales Data ---
print("Generating sales...")
sales_list = []
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 6, 30)
current_date = start_date

while current_date <= end_date:
    # Simulate a random number of sales per day
    for _ in range(random.randint(5, 20)):
        product = random.choice(product_list)
        sales_list.append({
            'order_id': fake.uuid4(),
            'order_date': current_date.date(),
            'customer_id': random.choice(customer_list)['customer_id'],
            'product_id': product['product_id'],
            'quantity': random.randint(1, 10),
            'unit_price': product['unit_price']
        })
    current_date += timedelta(days=1)

sales_df = pd.DataFrame(sales_list)
# Calculate total sales
sales_df['total_sale'] = sales_df['quantity'] * sales_df['unit_price']
sales_df.to_csv('sales.csv', index=False)

print("--- Phase 1 Complete! ---")
print("Generated products.csv, customers.csv, and sales.csv")