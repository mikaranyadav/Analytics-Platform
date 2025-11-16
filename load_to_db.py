import toml
import os
import pandas as pd
from sqlalchemy import create_engine, text

# --- 1. DEFINE DATABASE CONNECTION ---
# Load secrets from the .streamlit/secrets.toml file
secrets_path = os.path.join(".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

DB_USER = 'postgres'
DB_PASSWORD = secrets['database']['password']  # <-- Gets password from file
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'daimler_db'

# Create a connection "engine"
# This is how pandas will connect to our database
db_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_url)

print("Database engine created.")

# --- 2. DEFINE THE DATA MODEL (TABLE CREATION SQL) ---
# This is our "Data Model" blueprint
# We run this SQL to create the tables *before* we load any data

# We use "IF EXISTS" so we can re-run this script without errors
# We use CASCADE to handle dependencies (the foreign keys)
drop_tables_sql = """
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
"""

# SQL for creating the Products "dimension" table
create_products_sql = """
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    unit_price NUMERIC(10, 2)
);
"""

# SQL for creating the Customers "dimension" table
create_customers_sql = """
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255),
    country VARCHAR(100)
);
"""

# SQL for creating the Sales "fact" table
# It links to the dimension tables using FOREIGN KEYs
create_sales_sql = """
CREATE TABLE fact_sales (
    order_id VARCHAR(255) PRIMARY KEY,
    order_date DATE,
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    unit_price NUMERIC(10, 2),
    total_sale NUMERIC(12, 2),
    FOREIGN KEY (customer_id) REFERENCES dim_customers (customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_products (product_id)
);
"""

# --- 3. IMPLEMENT THE DATA PIPELINE ---

try:
    # Connect to the database
    with engine.connect() as conn:
        print("Connection established.")
        
        # --- Part A: (Re)Create the Data Model ---
        print("Dropping old tables (if they exist)...")
        conn.execute(text(drop_tables_sql))
        
        print("Creating table dim_products...")
        conn.execute(text(create_products_sql))
        
        print("Creating table dim_customers...")
        conn.execute(text(create_customers_sql))
        
        print("Creating table fact_sales...")
        conn.execute(text(create_sales_sql))
        
        conn.commit() # Commit the table creation
        print("All tables created successfully.")

        # --- Part B: Load CSV Data into Tables ---
        
        # Load Products
        print("Loading products.csv...")
        products_df = pd.read_csv('products.csv')
        products_df.to_sql('dim_products', engine, if_exists='append', index=False)
        
        # Load Customers
        print("Loading customers.csv...")
        customers_df = pd.read_csv('customers.csv')
        customers_df.to_sql('dim_customers', engine, if_exists='append', index=False)
        
        # Load Sales
        print("Loading sales.csv...")
        sales_df = pd.read_csv('sales.csv')
        sales_df.to_sql('fact_sales', engine, if_exists='append', index=False)
        
        print("All data loaded successfully.")

    print("\n--- PHASE 2 COMPLETE! ---")
    print("Data model created and all data loaded into daimler_db.")

except Exception as e:
    print(f"\nAn error occurred: {e}")