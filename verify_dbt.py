from google.cloud import bigquery
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/usr/app/service-account.json"

client = bigquery.Client()

# Query the DBT result table
query = """
    SELECT * 
    FROM `cohesive-poet-477209-h9.data_devops_dbt.avg_scores` 
    LIMIT 20
"""

print(f"Running query: {query}")
query_job = client.query(query)

print("\n--- RESULTS (Top 20) ---")
for row in query_job:
    print(dict(row))
print("------------------------")
