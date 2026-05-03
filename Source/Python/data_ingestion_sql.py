import pandas as pd
import sqlite3
import os

def ingest_data_to_sql():
    """
    Reads the professional incident CSV and loads it into a SQLite database.
    Prepares the schema including the AI Analysis column for the orchestration phase.
    """
    csv_path = 'Data/Raw/incident_data.csv'
    db_path = 'Data/Processed/global_incidents.db'
    
    # 1. Extract
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please run the generator first.")
        return

    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 2. Transform
    # Convert Timestamp strings to actual datetime objects for better SQL handling
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # IMPORTANT: Create the 'ai_analysis' column as empty (None/NULL) 
    # This prepares the table schema for the AI Orchestrator
    df['ai_analysis'] = None
    
    # 3. Load
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    try:
        # Load data into 'incidents' table
        # if_exists='replace' ensures a clean, professional start for your portfolio
        df.to_sql('incidents', conn, if_exists='replace', index=False)
        print(f"Success: {len(df)} professional records loaded into {db_path}")
        print("Table 'incidents' is now ready for AI Orchestration.")
        
    except Exception as e:
        print(f"Error during SQL ingestion: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    ingest_data_to_sql()