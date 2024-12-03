

## build image
docker build -t stream-sensor-collector .
docker run -it --rm --network host stream-sensor-collector:latest
# build and push docker hub
docker build -t e4espootin/stream-sensor-collector .
docker push e4espootin/stream-sensor-collector



# docker run
docker run -it --rm -d --network host --name stream-sensor-collector e4espootin/stream-sensor-collector 
# python run
python main.py 

# verify connection
docker exec -it container1 ping container2

## pull
docker pull e4espootin/stream-sensor-collector:latest
docker run -it --rm --network host --name stream-sensor-collector e4espootin/stream-sensor-collector:latest 