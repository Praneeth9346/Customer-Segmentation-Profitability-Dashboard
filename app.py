import streamlit as st
import plotly.express as px
import pandas as pd
from src.db_manager import DatabaseManager
from src.data_generator import generate_dummy_data

# --- CONFIG ---
st.set_page_config(page_title="Retail Insights", layout="wide")
st.title("📊 Customer Segmentation & Profitability Dashboard")

# Initialize DB
db = DatabaseManager()

# --- SIDEBAR: DATA CONTROLS ---
st.sidebar.header("Data Settings")

# Check if table exists by trying a simple query
check_df = db.run_query("SELECT name FROM sqlite_master WHERE type='table' AND name='orders';")

if check_df.empty:
    st.warning("⚠️ Database is empty! Click the button in the sidebar to generate data.")
    if st.sidebar.button("🚀 Generate & Load Dummy Data"):
        with st.spinner("Generating 1500 rows of synthetic data..."):
            # 1. Generate Data in Memory
            df = generate_dummy_data()
            # 2. Load to SQL
            success, msg = db.load_dataframe_to_db(df)
            if success:
                st.sidebar.success(msg)
                st.rerun() # Refresh app to show data
            else:
                st.sidebar.error(msg)
    st.stop() # Stop execution here until data is loaded

# If we get here, the data exists!
if st.sidebar.button("🔄 Reset Data"):
    df = generate_dummy_data()
    db.load_dataframe_to_db(df)
    st.rerun()

# --- DASHBOARD LOGIC (Only runs if data exists) ---

# 1. KPI SECTION (SQL Aggregations)
st.subheader("Executive Overview")
kpi_df = db.run_query("SELECT SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit FROM orders")

if not kpi_df.empty and kpi_df.iloc[0,0] is not None:
    sales = kpi_df.iloc[0,0]
    profit = kpi_df.iloc[0,1] # Fixed index
    margin = (profit / sales) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${sales:,.2f}")
    c2.metric("Total Profit", f"${profit:,.2f}")
    c3.metric("Profit Margin", f"{margin:.1f}%")
else:
    st.error("Error reading KPIs. Try resetting data.")

st.markdown("---")

# 2. VISUALIZATIONS
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

# 3. ADVANCED SQL: RFM SEGMENTATION
st.markdown("---")
st.subheader("👥 Customer Segmentation (RFM Analysis)")
st.caption("Using SQL to aggregate customer value and Python for segmentation logic.")

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

# Business Logic
def segment_customer(row):
    if row['Monetary'] > 3000 and row['Frequency'] > 8:
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
                      color_discrete_map={'🥇 Gold (VIP)': '#FFD700', '🥈 Silver (Regular)': '#C0C0C0', '🥉 Bronze (New/Low)': '#CD7F32'})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.write("**Top VIP Customers**")
        vip_df = df_rfm[df_rfm['Segment'] == '🥇 Gold (VIP)'].sort_values('Monetary', ascending=False).head(5)
        st.dataframe(vip_df, use_container_width=True)
