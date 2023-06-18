import os
from waitress import serve
from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__)

my_secret = os.environ['pocky_key']

class WeatherStack:
    def __init__(self):
        self.base_url = "http://api.weatherstack.com/"
        self.api_key = my_secret

    def get_current_weather(self, locations, units="m"):
        endpoint = self.base_url + "current"
        locations = ";".join(locations)
        params = {
            "access_key": self.api_key,
            "query": locations,
            "units": units
        }
        response = requests.get(endpoint, params=params)
        data = response.json()
        return data

@app.route('/weather/current', methods=['GET'])
def get_current_weather():
    locations = request.args.get('locations').split(',')
    ws = WeatherStack()
    data = ws.get_current_weather(locations)
    return jsonify(data)

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
