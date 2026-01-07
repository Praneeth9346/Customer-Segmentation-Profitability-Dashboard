import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name="retail.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def load_csv_to_db(self, csv_path):
        # Load CSV to Pandas first
        df = pd.read_csv(csv_path, encoding='windows-1252') # Common encoding for Superstore
        
        # Clean column names (remove spaces)
        df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]
        
        # Dump to SQL
        df.to_sql('orders', self.conn, if_exists='replace', index=False)
        return "Data Loaded to SQL Successfully!"

    def run_query(self, query):
        return pd.read_sql(query, self.conn)