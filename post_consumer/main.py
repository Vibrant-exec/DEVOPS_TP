import logging
import json
import os
import argparse
from kafka import KafkaConsumer
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# BigQuery Schema
SCHEMA = [
    bigquery.SchemaField('id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('post_type_id', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('accepted_answer_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('creation_date', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('score', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('view_count', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('body', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('owner_user_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('last_editor_user_id', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('last_edit_date', 'TIMESTAMP', mode='NULLABLE'),
    bigquery.SchemaField('last_activity_date', 'TIMESTAMP', mode='NULLABLE'),
    bigquery.SchemaField('title', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('tags', 'STRING', mode='NULLABLE'),
    bigquery.SchemaField('answer_count', 'INTEGER', mode='NULLABLE'),
    bigquery.SchemaField('comment_count', 'INTEGER', mode='REQUIRED'),
    bigquery.SchemaField('content_license', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('parent_id', 'STRING', mode='NULLABLE')
]

def create_dataset_if_not_exists(client, dataset_id, project_id):
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        log.info(f"Dataset {dataset_id} already exists.")
    except Exception:
        log.info(f"Dataset {dataset_id} does not exist. Creating it.")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"
        client.create_dataset(dataset)
        log.info(f"Created dataset {dataset_id}.")

def get_table(client, dataset_id, table_id):
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        table = client.get_table(table_ref)
        log.info(f"Table {table_id} already exists.")
        return table
    except Exception:
        log.info(f"Table {table_id} does not exist. Creating it.")
        table = bigquery.Table(table_ref, schema=SCHEMA)
        return client.create_table(table)

def insert_rows(client, table, rows):
    errors = client.insert_rows(table, rows)
    if not errors:
        log.info(f"Inserted {len(rows)} rows.")
    else:
        log.error(f"Encountered errors while inserting rows: {errors}")

def main(kafka_host, topic, dataset_id, table_id):
    # BigQuery Client
    # Credentials are implicitly read from GOOGLE_APPLICATION_CREDENTIALS env var
    client = bigquery.Client()
    project_id = client.project
    
    create_dataset_if_not_exists(client, dataset_id, project_id)
    table = get_table(client, dataset_id, table_id)

    # Kafka Consumer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[kafka_host],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='bq-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    log.info(f"Listening on {topic} from {kafka_host}...")

    for message in consumer:
        log.info(f"Received message: {message.value}")
        try:
            insert_rows(client, table, [message.value])
        except Exception as e:
            log.error(f"Failed to process message: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--kafka_host', type=str, required=True, help='Kafka Broker Host')
    parser.add_argument('--topic', type=str, default='posts', help='Kafka Topic')
    parser.add_argument('--dataset', type=str, default='data_devops', help='BigQuery Dataset')
    parser.add_argument('--table', type=str, default='posts', help='BigQuery Table')
    
    args = parser.parse_args()

    main(args.kafka_host, args.topic, args.dataset, args.table)
