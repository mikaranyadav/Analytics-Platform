# Enterprise Financial Analytics Platform (Daimler Case Study)

This project is a complete, end-to-end data platform that simulates and analyzes financial sales data. The goal was to build a system that can take raw sales information (like from an SAP system), process it, store it in a central database, and then display key financial insights on an interactive dashboard for business leaders.

The entire system is built using free, open-source tools.

## 📈 Dashboard Preview

Here is a screenshot of the final interactive dashboard, which visualizes our key financial metrics.

https://github.com/mikaranyadav/Analytics-Platform/blob/main/dashboard-preview.png
https://github.com/mikaranyadav/Analytics-Platform/blob/main/dashboard-preview1.png
https://github.com/mikaranyadav/Analytics-Platform/blob/main/dashboard-preview2.png

---

## 💡 What This Project Does

Think of this project as building a fully automated factory line for data:

1.  **🏭 Step 1: Create Raw Materials (Data Simulation)**
    * We can't use real, sensitive company data, so we first *simulate* it.
    * The `generate_data.py` script acts like a fake SAP system, creating thousands of realistic but random sales records, customer details, and product lists. It saves these as CSV files.

2.  **🚚 Step 2: Build the Warehouse & Pipeline (Data Engineering)**
    * We build a "data warehouse" (a central database) using **PostgreSQL** to store all our data cleanly.
    * The `load_to_db.py` script is our "pipeline." It picks up the raw CSV files, cleans them, and loads them into the correct tables in our database. This makes the data organized and ready for analysis.

3.  **📊 Step 3: Ask Questions (Data Analysis)**
    * With our data warehouse full, we use **SQL** (the language of databases) to ask complex questions, such as:
        * "What is our total revenue per quarter?"
        * "Who are our top 10 most valuable customers?"
        * "Which product categories are selling the most?"

4.  **📺 Step 4: Tell the Story (Data Visualization)**
    * The `dashboard.py` file uses **Streamlit** to build an interactive web page.
    * This dashboard runs our SQL queries live and presents the answers as easy-to-understand charts and tables, allowing a non-technical user (like a manager) to see the company's performance at a glance.

---

## 🛠️ Tech Stack

* **Python:** The core language used for all scripts.
* **PostgreSQL:** Our free and powerful open-source database, which acts as the **data warehouse**.
* **Pandas:** A Python library used to build the data pipeline, making it easy to read the CSVs and load them into the database.
* **SQLAlchemy:** A Python library that helps Pandas communicate with our PostgreSQL database efficiently.
* **Faker:** A Python library used to generate the realistic, fake data for our simulation.
* **Streamlit:** A Python library used to build the interactive web-based dashboard (our free alternative to Power BI).
* **Plotly:** A Python library that helps Streamlit create beautiful, interactive charts.
* **pgAdmin 4:** The desktop tool used to manage and visually inspect our PostgreSQL database.

---

