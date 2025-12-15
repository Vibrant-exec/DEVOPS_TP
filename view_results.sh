#!/bin/bash

# Helper script to view the results in BigQuery using Python
# It uses the 'verify_dbt.py' script we created earlier.

echo "🔍 Fetching results from BigQuery (avg_scores)..."

docker run --rm \
  -v $(pwd):/usr/app \
  -w /usr/app \
  python:3.10-slim-bookworm \
  sh -c "pip install -q google-cloud-bigquery && python verify_dbt.py"
