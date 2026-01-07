import sqlite3
import pandas as pd
import streamlit as st

class DatabaseManager:
    def __init__(self, db_name="retail.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def load_csv_to_db(self, csv_path):
        """Loads the CSV data into a SQL Table"""
        try:
            df = pd.read_csv(csv_path)
            # Clean column names
            df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]
            
            # Dump to SQL (Replace table if exists)
            df.to_sql('orders', self.conn, if_exists='replace', index=False)
            return "✅ Data Successfully Loaded into SQLite Database!"
        except Exception as e:
            return f"❌ Error loading data: {e}"

    def run_query(self, query):
        """Executes a SQL query and returns a Pandas DataFrame"""
        try:
            return pd.read_sql(query, self.conn)
        except Exception as e:
            st.error(f"SQL Error: {e}")
            return pd.DataFrame()
