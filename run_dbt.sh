#!/bin/bash

# Helper script to run DBT transformations using Docker
# This wraps the complex volume mounting and path handling

echo "🚀 Starting DBT Transformation..."

docker run --rm \
  -v $(pwd)/dbt_transform:/usr/app \
  -v $(pwd)/service-account.json:/usr/app/service-account.json \
  ghcr.io/dbt-labs/dbt-bigquery:1.5.0 run --profiles-dir /usr/app

echo "✅ DBT Run Complete."
