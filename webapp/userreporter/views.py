from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

import requests 
import pandas as pd
import numpy as np
import pickle
import sklearn
import json
from pprint import pprint

from userreporter.models import Fire
from userreporter.dc_models import FIRE_CLUSTERING, FIRE_AREA, FIRE_PROBA


def get_map(request):
    return render(request, 'index.html', locals())

@csrf_exempt
def post_confirm(request):
    if request.method == "POST":
        confermed = True if request.POST['confermed'] == 'true' else False
        lat = request.POST['lat']
        lng = request.POST['lng']
        get_features(lat, lng)
        print(Fire.objects.all())
        Fire.objects.filter(lat=float(lat), lng=float(lng)).update(is_active=confermed)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def post_predict_new_fire(request):
    if request.method == "POST":
        lat = request.POST['lat']
        lng = request.POST['lng']
        df = pd.DataFrame([get_features(lat, lng).to_pandas()])
        area = FIRE_AREA.predict_raw(df) * 10000
        data_proba = FIRE_PROBA.predict_proba(df)
        Fire.objects.update_or_create(lat=float(lat), lng=float(lng), range=area, is_active=True, probability=data_proba)
        return HttpResponse(json.dumps({'data': [lat, lng, area[0], data_proba[0]]}))
    return HttpResponse(status=404)


def get_fires(request):
    fires = Fire.objects.all()
    return HttpResponse(json.dumps({'data': [[fire.lat, fire.lng, fire.range, fire.is_active, fire.probability] for fire in fires]}))


def populate_base_on_start():
    centroids = FIRE_CLUSTERING.cluster_centers_
    df = pd.DataFrame(
        [get_features(centroid[0], centroid[1]).to_pandas()
         for centroid in centroids])
    area = FIRE_AREA.predict_raw(df) * 10000
    data_proba = FIRE_PROBA.predict_proba(df)

    concatenatedData = np.concatenate((centroids, np.reshape(area.T, (-1, 1))), axis=1)
    concatenatedData = np.concatenate((concatenatedData, np.reshape(data_proba[:, 1], (-1, 1))), axis=1)
    dbObjects = []

    for entry in concatenatedData:
        dbObjects.append(Fire(lat=entry[0], lng=entry[1], range=entry[2], is_active=False, probability=entry[3]))
    try:
        Fire.objects.bulk_create(dbObjects)
    except IntegrityError as e:
        pass


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

