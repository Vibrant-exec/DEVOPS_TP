# Data DevOps Data Pipeline

## Overview
This project implements a complete data pipeline on Kubernetes, connecting a data producer to Google BigQuery via Kafka, with transformations managed by DBT and deployment managed by ArgoCD (GitOps).

## Architecture
```mermaid
graph LR
    Pusher[Post Pusher] -->|JSON Messages| Kafka
    Kafka -->|Topic: posts| Consumer[Post Consumer]
    Consumer -->|Insert Rows| BQ[(BigQuery)]
    DBT[DBT Transformation] -->|SQL| BQ
```

## Deployment Components
All Kubernetes manifests are located in the `k8s/` directory and managed via ArgoCD.

*   **Infrastructure**: Kafka, Kafka UI
*   **Apps**: Post Pusher, Post Consumer
*   **GitOps**: ArgoCD

## CI/CD Pipeline (GitHub Actions)
Every push to `main` triggers a workflow that:
1.  Builds Docker images for `post_pusher` and `post_consumer`.
2.  Pushes them to **GitHub Container Registry (GHCR)**.
3.  ArgoCD detects the new images (if tags change or if set to Always pull) and updates the cluster.

## Setup & Installation

### 1. Prerequisites
*   Kubernetes Cluster (Kind or K3s)
*   Google Cloud Service Account (`service-account.json`) with BigQuery Admin roles.

### 2. Secrets Management (Important)
The consumer requires a GCP key to write to BigQuery.
1.  Copy `k8s/post_consumer-secret.example.yaml` to `k8s/post_consumer-secret.yaml` (this file is ignored by Git).
2.  Base64 encode your `service-account.json` (`cat service-account.json | base64 -w 0`).
3.  Paste the result into `post_consumer-secret.yaml`.
4.  Apply manually: `kubectl apply -f k8s/post_consumer-secret.yaml`.

### 3. Deploy via ArgoCD
The project is configured to sync automatically using the GitOps pattern.
1.  **Install ArgoCD**: Deployed in `argocd` namespace.
2.  **Sync**: The `data-pipeline` Application watches the `k8s/` folder of this repository.

## Usage Guide

### 🅰️ Accessing ArgoCD
Monitor your deployment status.
```bash
# 1. Port Forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 2. Open Browser
# https://localhost:8080
# User: admin
# Password: (Get from secret: kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

### 🅱️ Running DBT (Transformations)
To execute the SQL transformations (calculate average scores from the raw posts):
```bash
# Run generic model
docker run --rm -v $(pwd):/usr/app -w /usr/app ghcr.io/dbt-labs/dbt-bigquery:latest run --project-dir dbt_transform --profiles-dir dbt_transform
```

### 🅲 Accessing Kafka UI
Debug message flow.
```bash
kubectl port-forward svc/kafka-ui-service 8081:8080
# Access at http://localhost:8081
```