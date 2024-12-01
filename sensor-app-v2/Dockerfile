FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#RUN apt-get update && apt-get install -y wget gnupg2
# RUN wget https://downloads.apache.org/kafka/3.9.0/kafka_2.12-3.9.0.tgz
# RUN tar xzf kafka_2.12-3.9.0.tgz 
# RUN mv kafka_2.12-3.9.0 /app/kafka-client
# RUN apt update
# RUN apt install -y default-jre
# RUN java -version

CMD ["python", "main.py", "--broker", "192.168.0.108", "--port", "9092"]


