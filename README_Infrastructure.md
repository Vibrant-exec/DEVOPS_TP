# Infrastructure: Kafka & Kafka-UI

## Description
Ce module met en place l'infrastructure de messagerie nécessaire pour le pipeline de données. Il déploie un cluster Kafka (single-node pour cet environnement de dev/test) et une interface graphique Kafka-UI pour visualiser les topics et messages.

## Contenu
- `kafka-broker-deployment.yaml` : Déploiement Kubernetes pour le broker Kafka.
- `kafka-broker-service.yaml` : Service pour exposer le broker Kafka au sein du cluster.
- `kafka-ui-deployment.yaml` : Déploiement pour l'interface de gestion.
- `kafka-ui-service.yaml` : Service pour accéder à l'UI.

## Pourquoi cette architecture ?
- **Kafka** : Choisi comme bus de messages pour découpler le producteur (post_pusher) du consommateur (post_consumer), assurant la résilience et la capacité de gérer des pics de charge.
- **Kafka-UI** : Essentiel pour le débogage et la surveillance visuelle des messages transitant dans le topic `posts`.
- **Kubernetes** : L'ensemble est conteneurisé pour répondre aux exigences de portabilité et de déploiement "à froid".

## Déploiement
```bash
kubectl apply -f k8s/kafka-deployment.yaml
kubectl apply -f k8s/kafka-service.yaml
kubectl apply -f k8s/ui-deployment.yaml # Renommé pour clarté si nécessaire
# ... ou simplement
kubectl apply -f k8s/
```
