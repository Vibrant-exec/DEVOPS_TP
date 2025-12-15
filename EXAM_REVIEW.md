# Kubernetes & GitOps Exam Review Guide

This guide connects the **Concepts** you learned to the **Files** in this project. Use this to revise.

## 1. Containerization (Docker)
**Concept**: Packaging code and dependencies into a portable unit.
*   **Influencing Files**:
    *   `post_pusher/Dockerfile`: Defines the Producer environment.
    *   `post_consumer/Dockerfile`: Defines the Consumer environment.
    *   `.github/workflows/deploy.yml`: The automation that builds these files and pushes them to the registry (GHCR).

## 2. Configuration (Decoupling)
**Concept**: Separating code from configuration (12-Factor App).
*   **Influencing Files**:
    *   `k8s/post_pusher-configmap.yaml`: Sets `KAFKA_HOST`. If you change this, the pusher talks to a different broker.
    *   `k8s/post_consumer-configmap.yaml`: Sets Topic names and BigQuery dataset names.
    *   `k8s/post_consumer-secret.yaml`: (**Critical**) Stores the GCP Service Account Key. This is injected as a file volume at `/etc/secrets`.

## 3. Infrastructure (Kafka)
**Concept**: Microservices communication.
*   **Influencing Files**:
    *   `k8s/kafka-deployment.yaml`: The actual Kafka broker application.
    *   `k8s/kafka-service.yaml`: Creates the internal DNS name (`kafka-service`) that other pods use to reach Kafka.

## 4. Workloads (Deployments)
**Concept**: Managing Pods, Replicas, and Updates.
*   **Influencing Files**:
    *   `k8s/post_pusher-deployment.yaml`: Runs the generator.
        *   *Key setting*: `imagePullPolicy: Always` (ensures CI/CD updates work).
    *   `k8s/post_consumer-deployment.yaml`: Runs the ingestion.
        *   *Key setting*: `replicas: 1` (Change this to scale up consumer capability).

## 5. GitOps (ArgoCD)
**Concept**: Git as the "Source of Truth".
*   **Influencing Files**:
    *   `argocd/application.yaml`: The Bridge. It tells ArgoCD: "Look at THIS GitHub Repo (`repoURL`) and make the cluster match the `k8s/` folder (`path`)."
    *   **Mechanism**: If you change a file in `k8s/` and push to Git, ArgoCD sees it and updates the cluster.

## 6. Transformations (DBT)
**Concept**: T (Transform) in ELT.
*   **Influencing Files**:
    *   `dbt_transform/models/avg_scores.sql`: The SQL logic.
    *   `dbt_transform/profiles.yml`: Connection settings to BigQuery.
