import streamlit as st
import plotly.express as px
from src.db_manager import DatabaseManager

# Config
st.set_page_config(page_title="Retail Insights", layout="wide")
db = DatabaseManager()

# Sidebar: Load Data
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload Superstore CSV", type=['csv'])

if uploaded_file:
    # Save temp file to load into DB
    with open("data/temp_data.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    status = db.load_csv_to_db("data/temp_data.csv")
    st.sidebar.success(status)

    # --- TAB 1: EXECUTIVE SUMMARY (SQL SKILLS) ---
    st.title("📊 Executive Sales Dashboard")
    
    # KPI Queries
    total_sales = db.run_query("SELECT SUM(Sales) as Total FROM orders").iloc[0,0]
    total_profit = db.run_query("SELECT SUM(Profit) as Total FROM orders").iloc[0,0]
    profit_margin = (total_profit / total_sales) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"${total_sales:,.2f}")
    c2.metric("Total Profit", f"${total_profit:,.2f}")
    c3.metric("Profit Margin", f"{profit_margin:.2f}%")

    # SQL Aggregation for Charts
    # "Which Region is most profitable?"
    df_region = db.run_query("""
        SELECT Region, SUM(Sales) as Sales, SUM(Profit) as Profit 
        FROM orders 
        GROUP BY Region 
        ORDER BY Profit DESC
    """)
    
    st.subheader("Regional Performance")
    fig = px.bar(df_region, x="Region", y=["Sales", "Profit"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: RFM ANALYSIS (ANALYTICAL SKILLS) ---
    st.markdown("---")
    st.title("👥 Customer Segmentation (RFM)")
    
    # RFM Query: The complex part!
    # Recency: Days since last order
    # Frequency: Count of orders
    # Monetary: Sum of Sales
    rfm_query = """
    SELECT 
        Customer_ID, 
        MAX(Order_Date) as Last_Order_Date,
        COUNT(DISTINCT Order_ID) as Frequency,
        SUM(Sales) as Monetary
    FROM orders
    GROUP BY Customer_ID
    """
    df_rfm = db.run_query(rfm_query)
    
    # Simple Segmentation Logic (Python)
    # In a real job, you'd use quantiles, but here's a simple rule-based approach:
    # High Value: Frequency > 5 AND Monetary > 1000
    def segment_customer(row):
        if row['Frequency'] >= 5 and row['Monetary'] > 2000:
            return 'Gold (Loyal)'
        elif row['Frequency'] >= 2:
            return 'Silver (Regular)'
        else:
            return 'Bronze (New/Churned)'

    df_rfm['Segment'] = df_rfm.apply(segment_customer, axis=1)

    c1, c2 = st.columns(2)
    with c1:
        st.write("Customer Segments Distribution")
        fig_pie = px.pie(df_rfm, names='Segment', title="Customer Segments")
        st.plotly_chart(fig_pie)
    
    with c2:
        st.write("Top 5 'Gold' Customers")
        st.dataframe(df_rfm[df_rfm['Segment'] == 'Gold (Loyal)'].sort_values('Monetary', ascending=False).head(5))

else:
    st.info("Please upload the Superstore CSV to begin.")