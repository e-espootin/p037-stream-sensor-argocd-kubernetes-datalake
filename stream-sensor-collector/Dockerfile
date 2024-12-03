FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ENV AWS_ACCESS_KEY_ID=x
# ENV AWS_SECRET_ACCESS_KEY=y

CMD ["python", "main.py"]


