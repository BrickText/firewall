from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests 

from pprint import pprint
from weather import Weather, Unit


def get_map(request):
    return render(request, 'index.html',  locals())

@csrf_exempt
def post_confirm(request):
    if request.method == "POST":
        confermed = request.POST['confermed']
        lat = request.POST['lat']
        lng = request.POST['lng']
        get_features(lat, lng)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def get_features(lat, lng):
    url = "http://api.apixu.com/v1/current.json?key=ad23cdc4a1404d34984174745182010&q=" + lat + "," + lng
    r = requests.get(url).json()['current']
    dataSample = DataSetSample(r['humidity'], r['temp_c'], r['wind_kph'], r['precip_mm'])
    print(dataSample)


class DataSetSample:

    def __init__(self, humidity, temp, wind_speed, rain_per_mm):
        self.humidity = float(humidity)
        self.temp = float(temp)
        self.wind_speed = float(wind_speed)
        self.rain_per_mm = float(rain_per_mm)

    def __str__(self):
        return ("Humidity: " + str(self.humidity) + " Temperature: " + str(self.temp) + " Wind speed: " +
            str(self.wind_speed) + " Rain per m^2:" + str(self.rain_per_mm))