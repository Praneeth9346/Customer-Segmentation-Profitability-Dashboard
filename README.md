# 📊 Customer Segmentation & Profitability Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![SQL](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)

A full-stack data analytics project that transforms raw retail data into actionable business insights. This interactive dashboard allows stakeholders to identify high-value customers through **RFM Analysis** (Recency, Frequency, Monetary) and pinpoint profitability trends across different regions and product categories.

## 🚀 Features

### 1. 📈 Executive Sales Dashboard
* **KPI Tracking:** Real-time calculation of Total Revenue, Total Profit, and Profit Margins.
* **Regional Analysis:** Interactive bar charts visualizing which regions are driving the most profit.
* **Category Performance:** Breakdown of sales volume by product category (Furniture, Technology, etc.).

### 2. 👥 Advanced Customer Segmentation (RFM)
* **SQL-Powered Aggregation:** Uses complex SQL queries to calculate customer lifetime value metrics.
* **Automatic Segmentation:** Categorizes customers into segments based on purchasing behavior:
    * 🥇 **Gold (VIP):** High spenders with frequent orders.
    * 🥈 **Silver (Regular):** Consistent buyers with moderate spend.
    * 🥉 **Bronze (New/Low):** Low frequency or one-time buyers.
* **Actionable Insights:** Generates lists of top VIP customers for targeted marketing campaigns.

### 3. 💾 Automated Data Pipeline
* **Synthetic Data Generation:** Includes a Python module (`src/data_generator.py`) to generate realistic e-commerce datasets on the fly.
* **ETL Process:** Automatically extracts data, transforms it, and loads it into a persistent SQLite database for efficient querying.

## 🛠️ Tech Stack

* **Language:** Python
* **Database:** SQLite (SQL)
* **Dashboard Framework:** Streamlit
* **Visualization:** Plotly Express
* **Data Manipulation:** Pandas, NumPy
  
## 📂 Project Structure

```text
Customer-Segmentation-Profitability-Dashboard/
├── src/
│   ├── db_manager.py        # Handles SQL connections and queries
│   └── data_generator.py    # Generates synthetic e-commerce data
├── app.py                   # Main Streamlit Dashboard application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
💻 Installation & Usage
Clone the Repository

Bash

git clone [https://github.com/Praneeth9346/Customer-Segmentation-Profitability-Dashboard/tree/main]
cd Customer-Segmentation-Profitability-Dashboard
Install Dependencies

Bash

pip install -r requirements.txt
Run the App

Bash

streamlit run app.py
Initialize Data

Once the app opens in your browser, look for the warning "Database is empty!".

Click the "🚀 Generate & Load Dummy Data" button in the sidebar.

The app will generate 1,500 rows of transaction data and populate the SQL database automatically.

📊 Analytics Approach
This project moves beyond simple CSV analysis by implementing a robust "Data Analyst" workflow:

Ingest: Raw data is generated and loaded into a relational database (SQLite).

Query: Key metrics are derived using SQL aggregation queries (GROUP BY, SUM, COUNT) rather than just Pandas manipulation, mimicking real-world enterprise environments.

Visualize: Insights are rendered using interactive Plotly charts for user exploration.

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.
