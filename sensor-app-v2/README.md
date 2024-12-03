
## kafka
dev/docker-compose/kafka

## build image
docker build -t sensor-app-v2 .
# build and push docker hub
docker build -t e4espootin/sensor-app-v2 .
docker push e4espootin/sensor-app-v2



# docker run
docker run -it --rm -d --network host --name sensor-app-v2 e4espootin/sensor-app-v2 
# python run
python main.py --broker 192.168.0.108 --port 9092

# verify connection
docker exec -it container1 ping container2

## pull
docker pull e4espootin/sensor-app-v2:latest
docker run -it --rm --network host e4espootin/sensor-app-v2:latest 