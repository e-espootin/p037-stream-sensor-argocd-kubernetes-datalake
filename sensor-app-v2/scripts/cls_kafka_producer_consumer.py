from datetime import datetime
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic
# from kafka.errors import TopicAlreadyExistsError
import json
#import logging

class MyKafkaManager:
    def __init__(self, bootstrap_servers=['kafka:9092'], topic_name = "sensor-topic"    ):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None
        self.admin_client = None
        self.topic_name = topic_name

    def create_producer(self):
        try:
            print(f"info bootstrap: {self.bootstrap_servers}")

            self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

            # KafkaProducer(
            #     bootstrap_servers=self.bootstrap_servers,
            #     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            #     acks='0',
            #     retries=2,
            #     linger_ms=5,
            #     request_timeout_ms=10000,  # Add timeout
            #     retry_backoff_ms=1000
            #     # batch_size=32768,
            #     # compression_type='gzip',
            #     # max_in_flight_requests_per_connection=10

            # )
            return self.producer
        except Exception as e:
            print(f"Failed to create producer: {e}")
            

    

    def create_topic(self):
        print(f"Creating topic: {self.topic_name}")
        self.admin_client = AdminClient({'bootstrap.servers': self.bootstrap_servers})

        print(f"debug 001")
        try:
            # new_topic = NewTopic(name=self.topic_name, num_partitions=1, replication_factor=1)
            new_topic = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in [self.topic_name]]

            # self.admin_client.create_topics([new_topic])
            fs = self.admin_client.create_topics(new_topic)
            print(f"Topic '{self.topic_name}' created successfully")
        # except TopicAlreadyExistsError:
        #     print(f"Topic '{self.topic_name}' already exists")
        except Exception as e:
            print(f"Failed to create topic: {e}")
        
            

        
    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


    def send_message(self, topic, message: json):
        try:
            if not self.producer:
                print(f"Creating producer for topic: {topic}")
                self.create_producer()

            # send message
            # for data in message:
            print(f"Sending message: {message}")
            # Trigger any available delivery report callbacks from previous produce() calls
            self.producer.poll(0)

            #
            data = json.dumps(message)
            # Asynchronously produce a message. The delivery report callback will
            # be triggered from the call to poll() above, or flush() below, when the
            # message has been successfully delivered or failed permanently.
            future = self.producer.produce(self.topic_name, data.encode('utf-8'), callback=self.delivery_report)

            # Wait for any outstanding messages to be delivered and delivery report
            # callbacks to be triggered.
            self.producer.flush()
            print(f"Message has been sent successfuly!")
            return future
        except Exception as e: 
            print(f"Failed to send message: {e}")
            

    def create_consumer(self, group_id=None):
        print(f"Creating consumer for topic: {self.topic_name}")
        self.consumer = Consumer({
                'bootstrap.servers': self.bootstrap_servers,
                'group.id': 'mygroup',
                'auto.offset.reset': 'earliest'
            })

        
        # KafkaConsumer(
        #     self.topic_name,
        #     bootstrap_servers=self.bootstrap_servers,
        #     auto_offset_reset='earliest', #latest, earliest, none
        #     enable_auto_commit=True, # Automatically commit offsets
        #     group_id=group_id,
        #     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        # )
        print(f"Consumer for topic: {self.topic_name} created successfully")
        return self.consumer
    
    def consume_messages(self, timeout_seconds=120):
        
        try:
            print(f"Consuming messages from topic: {self.topic_name}")
            current_timestamp = datetime.now().timestamp() 

            #
            
            if not self.consumer:
                raise ValueError("Consumer not initialized. Call create_consumer first.")
            
            print(f"start reading messages from consumer...")
            messages = []
            # Poll messages from consumer
            
            for msg in self.consumer:
                #logging.info(f"offset position: {self.consumer.position(self.consumer.assignment().pop())}")
                messages.append(msg.value)
                print(f"Received message: {msg.value} from partition: {msg.partition} at offset: {msg.offset}")
                
                """ if self.consumer.position(self.consumer.assignment().pop()) % 100 == 0:
                    self.consumer.commit() # manually commit offsets
                    logging.info(f"Offset committed.") """


                if  (datetime.now().timestamp()  - current_timestamp) > timeout_seconds:
                    print(f"timeout_ms reached, stop consuming messages")
                    break
                

            print(f"Consumed {len(messages)} messages from topic: {self.topic_name}")

            return messages
        
        except Exception as e:
            print(f"Kafka error: {e}")

    

    def close(self):
        if self.producer:
            self.producer.close()
        if self.consumer:
            self.consumer.close()
        if self.admin_client:
            self.admin_client.close()
