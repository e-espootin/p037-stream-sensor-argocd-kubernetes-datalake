from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_weather_berlin():
    api_key = 'bd8b3dce0a905f2df4bcdcbf7a34618d'
    url = f'http://api.openweathermap.org/data/2.5/weather?q=Berlin&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        weather = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'city': data['name']
        }
        return jsonify(weather)
    else:
        return jsonify({'error': 'Could not retrieve weather data'}), response.status_code

if __name__ == '__main__':
    app.run(host='192.168.0.174', port=8009)