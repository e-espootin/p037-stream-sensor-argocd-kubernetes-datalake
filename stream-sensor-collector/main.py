import configparser
from scripts.cls_kafka_producer_consumer import MyKafkaManager
#import argparse
import os
import time


def read_config(file_path):
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read(file_path)
    return config

def consume_and_store_streams():
    # parser = argparse.ArgumentParser(description='Stream Sensor Collector')
    # parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
    # args = parser.parse_args()

    # Access secrets from environment variables
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    #
    config = read_config('config.ini')
    # if not(args.broker):
    kafka_broker = config['kafka']['bootstrap_servers']
    kafka_topic = config['kafka']['topic']
    consumer_group = config['kafka']['consumer-group']
    interval_sec = int(config['recurring']['interval_sec'])
    messages_batch_size = int(config['recurring']['messages_batch_size'])
    
    try:
        kafka_manager = MyKafkaManager(
            bootstrap_servers=kafka_broker,
            topic_name=kafka_topic,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            bucket_name="ebi-generalpurpose-bucket",
            s3_file_path="p037"
        )
        print(f"Kafka bootstrap: {kafka_manager.bootstrap_servers}")
        print(f"Kafka topic: {kafka_manager.topic_name}")
        
        # create consumer
        kafka_manager.create_consumer(  # create consumer
            group_id=consumer_group
            , auto_offset_reset="earliest"
            , auto_commit_enable=True
        )
        kafka_manager.consume_messages_Commit_manually(messages_batch_size)
        


            

    except Exception as e:
        print(f"Failed to consume messages: {e}")   



if __name__ == "__main__":
    consume_and_store_streams()

    # todo : upload into data lake