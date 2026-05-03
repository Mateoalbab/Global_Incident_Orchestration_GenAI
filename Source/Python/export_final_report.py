import pandas as pd
import sqlite3
import os
from datetime import datetime

def export_to_csv():
    """
    Extracts analyzed incidents from SQL and saves them as a CSV for Power BI.
    Provides traceability by logging the export event.
    """
    db_path = 'Data/Processed/global_incidents.db'
    output_path = 'Outputs/final_incident_report.csv'
    
    # 1. Connect and Extract
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM incidents WHERE ai_analysis IS NOT NULL"
    
    print(f"Extracting analyzed data from {db_path}...")
    df = pd.read_sql_query(query, conn)
    
    # 2. Export
    if not os.path.exists('Outputs'):
        os.makedirs('Outputs')
        
    df.to_csv(output_path, index=False)
    conn.close()
    
    # 3. Traceability Log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] SUCCESS: {len(df)} records exported to {output_path}")

if __name__ == "__main__":
    export_to_csv()