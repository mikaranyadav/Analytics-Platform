import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# --- 1. DATABASE CONNECTION ---
# IMPORTANT: Replace YOUR_PASSWORD_HERE with your actual PostgreSQL password
DB_USER = 'postgres'
DB_PASSWORD = 'root' 
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'daimler_db'

# Create the connection "engine"
db_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_url)

# --- 2. DATA LOADING FUNCTIONS (with Caching) ---
# st.cache_data tells Streamlit to "remember" the data
# and not re-run the query unless the code changes.

@st.cache_data
def fetch_data(query):
    """Fetches data from the database using a given query."""
    try:
        with engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# --- 3. DEFINE ALL OUR SQL QUERIES (from Phase 3) ---

# Query for KPIs
kpi_query = """
SELECT
    SUM(total_sale) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    AVG(total_sale) AS avg_order_value
FROM fact_sales;
"""

# Query for Revenue by Category
category_query = """
SELECT
    p.category,
    SUM(s.total_sale) AS total_revenue
FROM fact_sales s
JOIN dim_products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
"""

# Query for Top 10 Customers
top_customers_query = """
SELECT
    c.customer_name,
    c.country,
    SUM(s.total_sale) AS lifetime_value
FROM fact_sales s
JOIN dim_customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_name, c.country
ORDER BY lifetime_value DESC
LIMIT 10;
"""

# Query for Quarterly Sales
quarterly_sales_query = """
SELECT
    EXTRACT(YEAR FROM order_date) AS sales_year,
    EXTRACT(QUARTER FROM order_date) AS sales_quarter,
    SUM(total_sale) AS quarterly_revenue
FROM fact_sales
GROUP BY sales_year, sales_quarter
ORDER BY sales_year, sales_quarter;
"""

# Query for Top 10 Products
top_products_query = """
SELECT
    p.product_name,
    p.category,
    SUM(s.quantity) AS total_units_sold,
    SUM(s.total_sale) AS total_revenue
FROM fact_sales s
JOIN dim_products p ON s.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
"""

# --- 4. BUILD THE STREAMLIT DASHBOARD LAYOUT ---

# Set page config to "wide" mode for better layout
st.set_page_config(layout="wide")

st.title("Enterprise Financial Analytics Dashboard 📈")

# --- Load all data ---
kpi_data = fetch_data(kpi_query)
category_data = fetch_data(category_query)
top_customers_data = fetch_data(top_customers_query)
quarterly_sales_data = fetch_data(quarterly_sales_query)
top_products_data = fetch_data(top_products_query)

# --- A. Display Key Financial Metrics (KPIs) ---
st.header("Key Financial Metrics")

if not kpi_data.empty:
    total_revenue = kpi_data['total_revenue'].iloc[0]
    total_orders = kpi_data['total_orders'].iloc[0]
    avg_order_value = kpi_data['avg_order_value'].iloc[0]

    # Use columns to show KPIs side-by-side
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Average Order Value", f"${avg_order_value:,.2f}")
else:
    st.warning("Could not load KPI data.")

st.markdown("---") # Adds a horizontal line

# --- B. Display Charts ---
st.header("Visualizations")

col1, col2 = st.columns(2)

with col1:
    # Bar chart for Revenue by Category
    st.subheader("Revenue by Product Category")
    fig_category = px.bar(
        category_data,
        x="category",
        y="total_revenue",
        title="Total Revenue by Product Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    # Line chart for Quarterly Sales
    st.subheader("Quarterly Sales Performance")
    # We need to create a 'quarter_year' string for proper plotting
    quarterly_sales_data['quarter_year'] = quarterly_sales_data['sales_year'].astype(str) + '-Q' + quarterly_sales_data['sales_quarter'].astype(str)
    
    fig_quarterly = px.line(
        quarterly_sales_data,
        x="quarter_year",
        y="quarterly_revenue",
        title="Quarterly Revenue Trend",
        markers=True
    )
    fig_quarterly.update_xaxes(tickangle=45)
    st.plotly_chart(fig_quarterly, use_container_width=True)

st.markdown("---")

# --- C. Display Data Tables ---
st.header("Detailed Reports")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Customers (Lifetime Value)")
    st.dataframe(top_customers_data)

with col2:
    st.subheader("Top 10 Best-Selling Products")
    st.dataframe(top_products_data)