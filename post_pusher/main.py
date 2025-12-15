import logging
import random
import os
import json
import re
import time
import argparse
from kafka import KafkaProducer


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TOPIC = "posts"  # Name of the Kafka topic
# Schema simplified for JSON serialization
ALLOWED_COLUMNS = {
    'id', 'post_type_id', 'accepted_answer_id', 'creation_date', 'score',
    'view_count', 'body', 'owner_user_id', 'last_editor_user_id',
    'last_edit_date', 'last_activity_date', 'title', 'tags',
    'answer_count', 'comment_count', 'content_license', 'parent_id'
}



def transform_key(key):
    # Remove '@' and convert to snake_case
    key = key.replace('@', '')
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
    return key

def filter_post(post, allowed_columns):
    return {k: v for k, v in post.items() if k in allowed_columns}

def transform_and_filter_post(post, allowed_columns):
    transformed_post = {transform_key(k): v for k, v in post.items()}
    filtered_post = filter_post(transformed_post, allowed_columns)
    return filtered_post

def post_kafka(transformed_post, kafka_host):
    # Kafka configuration
    bootstrap_servers = [kafka_host]

    # Create Producer instance
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        # Produce and send a single message
        future = producer.send(TOPIC, transformed_post)
        record_metadata = future.get(timeout=10)
        print(f"Message delivered to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
    except Exception as e:
        print(f"Message delivery failed: {e}")
    finally:
        producer.close()

def main(multiple, kafka_host):
    # Load the post from the JSON file
    data_filepath = "./data/movies-stackexchange/json/posts.json"
    log.info(data_filepath)
    log.info(os.getcwd())
    
    try:
        with open(data_filepath, "r") as f:
            content = f.read()

        # Check if it's an LFS pointer (starts with "version https")
        if content.startswith("version https"):
             log.error("CRITICAL: Detected LFS pointer file in Docker image. The real data was not downloaded.")
             log.error("Please ensure the file is tracked as a regular git file or LFS is working in CI.")
             raise ValueError("LFS Pointer found instead of data.")

        log.info(f"File content preview (first 200 chars): {content[:200]}")
        posts = json.loads(content)
        log.info(f"Successfully loaded {len(posts)} posts from file.")
        
    except Exception as e:
        log.error(f"Failed to load dataset: {e}")
        raise e # Crash the app so we know it failed

    while True:
        post = random.choice(posts)

        # Transform the post for insertion
        transformed_post = transform_and_filter_post(post, ALLOWED_COLUMNS)
        
        post_kafka(transformed_post, kafka_host)

        if not args.multiple:
            break

        time.sleep(10)

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--multiple', action='store_true', help='Send multiple messages')
    parser.add_argument('--kafka_host', type=str, required=True, help='The Kafka host address')
    args = parser.parse_args()

    main(
        multiple=args.multiple,
        kafka_host=args.kafka_host
    )