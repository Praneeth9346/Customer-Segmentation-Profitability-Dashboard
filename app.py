import streamlit as st
import plotly.express as px
import pandas as pd
import os
from src.db_manager import DatabaseManager

# --- CONFIG ---
st.set_page_config(page_title="Retail Insights", layout="wide")
st.title("📊 Customer Segmentation & Profitability Dashboard")

# Initialize DB
db = DatabaseManager()

# --- SIDEBAR: DATA LOADING ---
st.sidebar.header("Data Setup")

# check if data exists
data_path = 'data/superstore.csv'
if os.path.exists(data_path):
    if st.sidebar.button("Load/Reset Database"):
        status = db.load_csv_to_db(data_path)
        st.sidebar.success(status)
else:
    st.sidebar.error("No data found! Run generate_data.py first.")

# --- MAIN DASHBOARD ---

# 1. KPI SECTION (SQL Aggregations)
st.subheader("Executive Overview")
try:
    # We use a try-block in case the DB is empty
    kpi_df = db.run_query("SELECT SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit FROM orders")
    
    if not kpi_df.empty and kpi_df.iloc[0,0] is not None:
        sales = kpi_df.iloc[0,0]
        profit = kpi_df.iloc[0,0]
        margin = (profit / sales) * 100

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Revenue", f"${sales:,.2f}")
        c2.metric("Total Profit", f"${profit:,.2f}")
        c3.metric("Profit Margin", f"{margin:.1f}%")
    else:
        st.info("Please click 'Load/Reset Database' in the sidebar.")
        st.stop()

except:
    st.warning("Database not initialized. Click button in sidebar.")
    st.stop()

st.markdown("---")

# 2. REGIONAL PERFORMANCE
c1, c2 = st.columns(2)

with c1:
    st.subheader("📍 Profitability by Region")
    df_region = db.run_query("SELECT Region, SUM(Profit) as Profit FROM orders GROUP BY Region ORDER BY Profit DESC")
    fig1 = px.bar(df_region, x='Region', y='Profit', color='Profit', color_continuous_scale='Viridis')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("📦 Sales by Category")
    df_cat = db.run_query("SELECT Category, SUM(Sales) as Sales FROM orders GROUP BY Category")
    fig2 = px.pie(df_cat, names='Category', values='Sales', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# 3. RFM CUSTOMER SEGMENTATION (The Advanced Part)
st.markdown("---")
st.subheader("👥 Customer Segmentation (RFM Analysis)")
st.markdown("Identifying **High-Value** customers vs. **Churn Risk** using SQL & Python.")

# The Complex Query
rfm_query = """
SELECT 
    Customer_ID,
    COUNT(Order_ID) as Frequency,
    SUM(Sales) as Monetary
FROM orders
GROUP BY Customer_ID
"""
df_rfm = db.run_query(rfm_query)

# Business Logic for Segmentation
def segment_customer(row):
    if row['Monetary'] > 3000 and row['Frequency'] > 10:
        return '🥇 Gold (VIP)'
    elif row['Monetary'] > 1000:
        return '🥈 Silver (Regular)'
    else:
        return '🥉 Bronze (New/Low)'

if not df_rfm.empty:
    df_rfm['Segment'] = df_rfm.apply(segment_customer, axis=1)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Segment Distribution**")
        fig3 = px.pie(df_rfm, names='Segment', color='Segment', 
                      color_discrete_map={'🥇 Gold (VIP)': 'gold', '🥈 Silver (Regular)': 'silver', '🥉 Bronze (New/Low)': '#cd7f32'})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.write("**Top 5 VIP Customers (Actionable List)**")
        vip_df = df_rfm[df_rfm['Segment'] == '🥇 Gold (VIP)'].sort_values('Monetary', ascending=False).head(5)
        st.dataframe(vip_df, use_container_width=True)
