#!/usr/bin/python3

from urllib.request import urlopen
import json

apikey="aa8135d64b32f422" # sign up here http://www.wunderground.com/weather/api/ for a key

url="http://api.wunderground.com/api/"+apikey+"/conditions/q/PA/WestChester.json"
meteo=urlopen(url).read()
meteo = meteo.decode('utf-8')
weather = json.loads(meteo)

for key, value in weather['current_observation'].items():
    print (key, value)