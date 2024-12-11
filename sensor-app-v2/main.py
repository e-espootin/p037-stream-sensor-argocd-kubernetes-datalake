import configparser
import time
import random
from scripts.cls_openWeatherMapApi import OpenWeatherMapAPIClass 
from scripts.cls_kafka_producer_consumer import MyKafkaManager
import json
import argparse


def read_config(file_path):
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read(file_path)
    return config

def get_random_city():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Indianapolis", "Columbus", "Fort Worth", "Charlotte", "Seattle", "Denver", "El Paso", "Detroit", "Washington", "Boston", "Memphis", "Nashville", "Portland", "Oklahoma City", "Las Vegas", "Baltimore", "Louisville", "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Mesa", "Kansas City", "Atlanta", "Long Beach", "Colorado Springs", "Raleigh", "Miami", "Virginia Beach", "Omaha", "Oakland", "Minneapolis", "Tulsa", "Arlington", "New Orleans", "Berlin"]
    return random.choice(cities)

def get_random_number():
    return random.randint(1, 1000)

def send_message(producer, topic, message):
    try:
        producer.send(topic, value=message)
        producer.flush()
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def main():
    try:
        # Initialize the parser
        parser = argparse.ArgumentParser(description="A sample script to demonstrate argument parsing.")
        # Define arguments
        parser.add_argument("--broker", type=str, required=True, help="kafka broker address")
        parser.add_argument("--port", type=int, required=False, help="port number")

        # Parse arguments
        args = parser.parse_args()
        print(f"Broker: {args.broker}")
        kafka_broker = args.broker + ":" + str(args.port)
       
        
        # Read the configuration file
        config = read_config('config.ini')
        if not(args.broker):
            kafka_broker = config['kafka']['bootstrap_servers']
        kafka_topic = config['kafka']['topic']
        interval_sec = int(config['recurring']['interval_sec'])

        print(f"Kafka broker: {kafka_broker}")
        print(f"Kafka topic: {kafka_topic}")
        print(f"Interval: {interval_sec}")

        # create or get existing topic
        kafka_class_instance = MyKafkaManager(kafka_broker, kafka_topic)
        print(f"broker: {kafka_class_instance.bootstrap_servers}")
        kafka_class_instance.create_topic()

        # get senor project id
        project_id = get_random_number()


        while(True):
            # get weather data
            open_weather_map_instance = OpenWeatherMapAPIClass()
            city = get_random_city()
            res_json = open_weather_map_instance.get_formatted_weather_data(city, project_id)
            print(f"Data for city: {city}, {res_json}")
            
            # send message
            kafka_class_instance.send_message(kafka_topic, res_json)
            print(f"Message sent for city: {city}")

            # wait for interval
            print(f"Waiting for {interval_sec} seconds...")
            time.sleep(interval_sec)
       
       
      


    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()