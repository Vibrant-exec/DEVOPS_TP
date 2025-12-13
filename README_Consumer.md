# Post Consumer

## Description
Le composant `post_consumer` lit les messages depuis Kafka et les insère dans Google BigQuery.

## Configuration
- **ConfigMap** (`post-consumer-config`) :
  - `KAFKA_HOST` : Adresse du broker Kafka.
  - `KAFKA_TOPIC` : Topic à écouter ("posts").
  - `BQ_DATASET` : Dataset BigQuery.
  - `BQ_TABLE` : Table BigQuery.
- **Secret** (`google-cloud-key`) :
  - Contient le fichier JSON de compte de service (`key.json`).
  - **IMPORTANT** : Vous devez remplacer la valeur placeholder dans `k8s/post_consumer-secret.yaml` par le contenu encodé en base64 de votre vrai fichier `service-account.json`.

## Déploiement
1. Build de l'image Docker :
   ```bash
   cd post_consumer
   docker build -t post_consumer:latest .
   # Si utilisation de Kind: kind load docker-image post_consumer:latest
   ```
2. Mise à jour du Secret :
   Mettez à jour `k8s/post_consumer-secret.yaml` avec votre clé.
3. Déploiement :
   ```bash
   kubectl apply -f k8s/post_consumer-secret.yaml
   kubectl apply -f k8s/post_consumer-configmap.yaml
   kubectl apply -f k8s/post_consumer-deployment.yaml
   ```

## Scalabilité
Le déploiement est conçu pour être scalable. Pour augmenter le nombre de consommateurs (dans le même consumer group Kafka) :
```bash
kubectl scale deployment post-consumer --replicas=3
```
K8s répartira les partitions Kafka entre les instances automatiquement.
