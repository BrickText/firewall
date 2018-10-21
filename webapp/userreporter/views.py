from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from userreporter.models import Fire
import requests 

import pandas as pd
import numpy as np
import pickle
import sklearn
import json

from pprint import pprint


def get_map(request):
    return render(request, 'index.html', locals())

@csrf_exempt
def post_confirm(request):
    if request.method == "POST":
        confermed = request.POST['confermed']
        lat = request.POST['lat']
        lng = request.POST['lng']
        get_features(lat, lng)
        Fire.objects.update_or_create(lat=float(lat), lng=float(lng), range=area, is_active=confermed)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def post_predict_new_fire(request):
    if request.method == "POST":
        lat = request.POST['lat']
        lng = request.POST['lng']
        df = pd.DataFrame([get_features(lat, lng).to_pandas()])
        with open('../models/svm.b', 'rb') as f:
            svm = pickle.load(f)
        area = svm.predict(df)
        area = np.exp(area) * 10000
        Fire.objects.update_or_create(lat=float(lat), lng=float(lng), range=area, is_active=True)
        return HttpResponse(json.dumps({'data': [lat, lng, area[0]]}))
    return HttpResponse(status=404)


def get_fires(request):
    fires = Fire.objects.all()
    return HttpResponse(json.dumps({'data': [[fire.lat, fire.lng, fire.range, fire.is_active] for fire in fires]}))


def get_features(lat, lng):
    url = "http://api.apixu.com/v1/current.json?key=ad23cdc4a1404d34984174745182010&q="\
        + str(lat) + "," + str(lng)
    req = requests.get(url).json()
    if 'error' in req:
        return DataSetSample(0, 0, 0, 0)
    r = req['current']
    dataSample = DataSetSample(r['humidity'], r['temp_c'], r['wind_kph'], r['precip_mm'])
    return dataSample


class DataSetSample(dict):

    def __init__(self, humidity, temp, wind_speed, rain_per_mm):
        super(dict, self).__init__()
        self['temp'] = float(temp)
        self['RH'] = float(humidity)
        self['wind'] = float(wind_speed)
        self['rain'] = float(rain_per_mm)

    def to_pandas(self):
        return pd.Series(self)

    def __str__(self):
        return ("Humidity: " + str(self.humidity) + " Temperature: " + str(self.temp) + " Wind speed: " +
            str(self.wind_speed) + " Rain per m^2:" + str(self.rain_per_mm))

