import sqlite3
import pandas as pd
import streamlit as st

class DatabaseManager:
    def __init__(self, db_name="retail.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def load_dataframe_to_db(self, df):
        """Loads a Pandas DataFrame directly to SQL"""
        try:
            # Clean column names
            df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]
            
            # Dump to SQL (Replace table if exists)
            df.to_sql('orders', self.conn, if_exists='replace', index=False)
            return True, "✅ Data Successfully Loaded into SQLite Database!"
        except Exception as e:
            return False, f"❌ Error loading data: {e}"

    def run_query(self, query):
        """Executes a SQL query and returns a Pandas DataFrame"""
        try:
            return pd.read_sql(query, self.conn)
        except Exception as e:
            # Return empty dataframe if table doesn't exist yet
            return pd.DataFrame()
