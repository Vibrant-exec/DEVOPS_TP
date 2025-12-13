# Post Pusher: The Producer

## Description
Le composant `post_pusher` est une application Python qui simule la création de "posts" et les envoie vers un topic Kafka.

## Rôle dans l'architecture
Il agit comme la source de données (Producer). Il lit un jeu de données local (JSON) et envoie périodiquement des messages aléatoires vers Kafka.

## Configuration
La configuration est externalisée via Kubernetes ConfigMaps :
- **KAFKA_HOST** : L'adresse du broker Kafka (injectée via la variable d'environnement `KAFKA_HOST` et passée en argument `--kafka_host`).

## Définition Kubernetes
- **Deployment** : `post_pusher-deployment.yaml`
  - Utilise l'image `post_pusher:latest`.
  - Lance le script `main.py` avec l'argument `--multiple` pour un envoi continu.
  - Ressource `Deployment` pour assurer la redondance et le redémarrage automatique.

## Build & Deploy
1. Build de l'image Docker :
   ```bash
   cd post_pusher
   docker build -t post_pusher:latest .
   # Si utilisation de Kind: kind load docker-image post_pusher:latest
   ```
2. Déploiement :
   ```bash
   kubectl apply -f k8s/post_pusher-configmap.yaml
   kubectl apply -f k8s/post_pusher-deployment.yaml
   ```
