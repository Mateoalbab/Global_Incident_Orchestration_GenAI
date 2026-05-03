import os
import sqlite3
import google.generativeai as genai
import time  # Library to manage security pauses (Rate Limiting)
from dotenv import load_dotenv

# 1. Infrastructure Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Using gemma-3-1b-it as detected in our initial audit for maximum efficiency
model = genai.GenerativeModel('models/gemma-3-1b-it')

def orchestrate_incidents():
    """
    Extracts pending incidents from SQL, analyzes them via Gemini AI, 
    and updates the database with insights.
    """
    db_path = 'Data/Processed/global_incidents.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. Data Extraction: Search for records without AI analysis
    # Batch size set to 100 for a solid Power BI sample
    cursor.execute("SELECT rowid, Description FROM incidents WHERE ai_analysis IS NULL LIMIT 100")
    rows = cursor.fetchall()

    if not rows:
        print("No new incidents found for analysis.")
        conn.close()
        return

    print(f"Starting orchestration for {len(rows)} incidents...")

    for row_id, description in rows:
        print(f"Analyzing Incident ID {row_id}...")
        
        # Structured prompt designed for Business Analysis
        prompt = f"""
        Act as a Senior Business Analyst. Analyze this IT incident: '{description}'
        Provide a concise analysis including:
        - Root Cause Category (Technical, Procedural, or Systemic)
        - Priority (1-5)
        - Suggested Process Improvement
        Keep the response under 50 words and well-structured.
        """
        
        try:
            # 3. AI Interaction
            response = model.generate_content(prompt)
            analysis = response.text.strip()
            
            # 4. Data Loading: Update the SQL database with insights
            cursor.execute("UPDATE incidents SET ai_analysis = ? WHERE rowid = ?", (analysis, row_id))
            conn.commit()
            print(f"Success: Record {row_id} updated.")
            
            # --- PROCESS IMPROVEMENT (Rate Limiting Management) ---
            # We wait 4 seconds to stay under the 15 requests/minute limit
            # enforced by the Google AI Studio Free Tier.
            time.sleep(4)
            
        except Exception as e:
            print(f"Error processing ID {row_id}: {e}")
            # If quota is hit, wait longer before the next attempt
            time.sleep(10)

    conn.close()
    print("\n--- Orchestration batch completed successfully ---")

if __name__ == "__main__":
    orchestrate_incidents()