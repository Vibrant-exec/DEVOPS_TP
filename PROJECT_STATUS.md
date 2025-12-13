xx# Project Status & Architecture Report

## 1. Overview
We have successfully implemented a complete Data Pipeline connecting a data producer to a data warehouse via a message bus, all hosted on Kubernetes.

**Flow**: `Post Pusher (App)` -> `Kafka (Message Bus)` -> `Post Consumer (App)` -> `BigQuery (Data Warehouse)`

## 2. What Has Been Done

### A. Infrastructure Layer
We deployed the core messaging infrastructure on Kubernetes.
- **Kafka Broker**: A single-node Kafka instance to handle message traffic.
    - *Manifests*: `k8s/kafka-deployment.yaml`, `k8s/kafka-service.yaml`
- **Kafka UI**: A web-based dashboard to visualize topics and messages.
    - *Manifests*: `k8s/kafka-ui-deployment.yaml`, `k8s/kafka-ui-service.yaml`
    - *Status*: Accessible via `localhost:8080` (requires port-forward).

### B. Producer Component (`post_pusher`)
We created an application that simulates data generation.
- **Code**: `post_pusher/main.py` reads a static JSON dataset (`posts.json`) and publishes messages to the `posts` Kafka topic.
- **Container**: Dockerized using `python:3.10`.
- **Configuration**:
    - Uses `k8s/post_pusher-configmap.yaml` to decouple the Kafka address (`kafka-broker-service:9092`).
    - Uses `k8s/post_pusher-deployment.yaml` with increased memory limits (**512Mi**) to handle the large dataset loading.

### C. Consumer Component (`post_consumer`)
We created an application that processes the data.
- **Code**: `post_consumer/main.py` listens to the `posts` Kafka topic and streams data into a Google BigQuery table.
- **Container**: Dockerized using `python:3.10`.
- **Security**: The Google Cloud Service Account Key is injected securely via a Kubernetes Secret (`k8s/post_consumer-secret.yaml`).
### D. Transformation Layer (DBT)
We installed and ran DBT to aggregate data.
- **Code**: `dbt_transform/` contains the SQL models (`avg_scores.sql`).
- **Execution**: Ran via Docker container `ghcr.io/dbt-labs/dbt-bigquery`.
- **Outcome**: Created `data_devops_dbt.avg_scores` table in BigQuery.

### E. GitOps Layer (ArgoCD)
We installed ArgoCD to manage the Kubernetes state.
- **Namespace**: `argocd`.
- **Application**: The `data-pipeline` app syncs the `k8s/` folder from this repo to the cluster.

## 3. Current Deployment Components (In `k8s/` folder)
| File | Purpose |
|------|---------|
| `kafka-deployment.yaml` | The data pipe (Kafka). |
| `kafka-service.yaml` | Network address for Kafka. |
| `kafka-ui-deployment.yaml` | The Dashboard. |
| `post_pusher-deployment.yaml` | The Sender app. |
| `post_consumer-deployment.yaml` | The Receiver app. |
| `post_consumer-secret.yaml` | GCP Credentials (**Ignored in Git**). |
| `post_consumer-secret.example.yaml` | Template for credentials. |

## 4. Ready for Expansion
This architecture is modular. Key areas for future work:
- **Scaling**: You can increase `replicas` in `post_consumer-deployment.yaml`.
- **CI/CD**: Add Github Actions to build docker images automatically.
