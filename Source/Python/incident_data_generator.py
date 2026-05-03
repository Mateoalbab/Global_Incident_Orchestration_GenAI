import pandas as pd
import random
import os
from datetime import datetime, timedelta

def generate_professional_incidents(num_records=1000):
    """
    Generates realistic IT incident data with full schema:
    Ticket_ID, Timestamp, Description, Region, Cost_Center, Initial_Severity.
    """
    # 1. Professional Data Pools
    systems = ["SAP ERP", "Active Directory", "VPN Gateway", "SQL Server", "Customer Portal", "Exchange Server", "Payroll System", "Network Firewall", "Inventory API", "Cloud Storage"]
    issues = ["timeout error", "high latency", "unauthorized access attempt", "connectivity failure", "database lock", "expired certificate", "service outage", "sync failure", "performance degradation"]
    locations = ["in Bogota Office", "in Cartagena Branch", "on the Cloud Cluster", "in the Finance Subnet", "during nightly backup", "in the Production Environment"]
    
    regions = ["LATAM", "NORTHAM", "EMEA", "APAC"]
    cost_centers = ["CC-ADMIN", "CC-LOGISTICS", "CC-IT-INFRA", "CC-FINANCE", "CC-SALES"]
    severities = ["Low", "Medium", "High", "Critical"]

    # 2. Date Range Configuration (Jan 1 to May 1, 2026)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 5, 1)
    time_delta = end_date - start_date

    data = []

    for i in range(num_records):
        # Generate random timestamp within range
        random_days = random.randint(0, time_delta.days)
        random_seconds = random.randint(0, 86400)
        timestamp = start_date + timedelta(days=random_days, seconds=random_seconds)
        
        # Assemble logical description
        description = f"{random.choice(systems)} reported a {random.choice(issues)} {random.choice(locations)}."
        
        data.append({
            "Ticket_ID": f"INC-{100000 + i}", # Sequential professional ID
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Description": description,
            "Region": random.choice(regions),
            "Cost_Center": random.choice(cost_centers),
            "Initial_Severity": random.choice(severities)
        })

    # 3. Export to CSV (Overwriting for consistency)
    output_path = "Data/Raw/incident_data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pd.DataFrame(data).to_csv(output_path, index=False)
    
    print(f"Success: 1,000 professional records generated at {output_path}")

if __name__ == "__main__":
    generate_professional_incidents(1000)