
## kafka
dev/docker-compose/kafka

## build image
docker build -t sensor-app-test1 .
# build and push docker hub
docker build -t e4espootin/sensor-app-test1 .
docker push e4espootin/sensor-app-test1

## docker run
docker run --network kafka_kafka-net sensor-app-test1

docker run \
  --name sensor-app-test1 \
  --network kafka_kafka-net \
  -p 9095:9094 \
  -p 9093:9092 \
  sensor-app-test1


# python run
python main.py --broker 192.168.16.2 --port 9094 

# verify connection
docker exec -it container1 ping container2

## pull
docker pull e4espootin/sensor-app-test1:latest
docker run -it --rm --network host e4espootin/sensor-app-test1:latest 