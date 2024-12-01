from typing import Union

from fastapi import FastAPI
import requests

app = FastAPI()
API_KEY = "bd8b3dce0a905f2df4bcdcbf7a34618d"

@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.get("/weather/{city_name}")
def get_weather(city_name: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "City not found"}