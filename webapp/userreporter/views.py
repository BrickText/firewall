import json

import numpy as np
import pandas as pd
import requests
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from userreporter.ml_models import FIRE_AREA, FIRE_CLUSTERING, FIRE_PROBA
from userreporter.models import Fire


# ====================================================================================================

def get_map(request):
    return render(request, 'index.html', locals())

# ====================================================================================================

@csrf_exempt
def post_confirm(request):
    if request.method == 'POST':
        confirmed = True if request.POST['confirmed'] == 'true' else False
        lat = round(float(request.POST['lat']), 5)
        lng = round(float(request.POST['lng']), 5)
        Fire.objects.filter(lat=lat, lng=lng).update(is_active=confirmed)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

# ====================================================================================================

@csrf_exempt
def post_predict_new_fire(request):
    if request.method == 'POST':
        lat = round(float(request.POST['lat']), 5)
        lng = round(float(request.POST['lng']), 5)

        df = pd.DataFrame([get_features(lat, lng).to_pandas()])
        data_proba = round(float(FIRE_PROBA.predict_proba(df)[0][1]), 5)
        area = float(FIRE_AREA.predict(df)[0] * 10000)

        Fire.objects.update_or_create(lat=lat, lng=lng, range=area, is_active=True, probability=data_proba)
        return HttpResponse(json.dumps({'data': [lat, lng, area, data_proba]}))

    return HttpResponse(status=404)

# ====================================================================================================

def get_fires(request):
    fires = Fire.objects.all()
    return HttpResponse(json.dumps(
        {'data': [[fire.lat, fire.lng, fire.range, str(fire.is_active), fire.probability] for fire in fires]}
    ))

# ====================================================================================================

def populate_base_on_start():
    centroids = FIRE_CLUSTERING.cluster_centers_
    df = pd.DataFrame(
        [get_features(centroid[0], centroid[1]).to_pandas()
         for centroid in centroids])

    data_proba = FIRE_PROBA.predict_proba(df)
    areas = FIRE_AREA.predict(df) * 10000

    concatenatedData = np.concatenate((centroids, np.reshape(areas.T, (-1, 1))), axis=1)
    concatenatedData = np.concatenate((concatenatedData, np.reshape(data_proba[:, 1], (-1, 1))), axis=1)

    dbObjects = []
    for entry in concatenatedData:
        dbObjects.append(
            Fire(lat=round(entry[0], 5), lng=round(entry[1], 5), range=entry[2], is_active=False, probability=entry[3])
        )
    try:
        Fire.objects.bulk_create(dbObjects)
    except IntegrityError:
        pass

# ====================================================================================================

def get_features(lat, lng):
    url = 'http://api.apixu.com/v1/current.json?key=ad23cdc4a1404d34984174745182010&q='\
        + str(lat) + ',' + str(lng)
    req = requests.get(url).json()

    if 'error' in req:
        return DataSetSample(0, 0, 0, 0)

    r = req['current']
    return DataSetSample(r['temp_c'], r['humidity'], r['wind_kph'], r['precip_mm'])

# ====================================================================================================

class DataSetSample(dict):
    def __init__(self, temp, humidity, wind_speed, rain_per_mm):
        super().__init__()
        self['temp'] = float(temp)
        self['RH'] = float(humidity)
        self['wind'] = float(wind_speed)
        self['rain'] = float(rain_per_mm)

    def to_pandas(self):
        return pd.Series(self)

    def __str__(self):
        return ('Temperature: ' + str(self['temp']) + 'Humidity: ' + str(self['RH']) + ' Wind speed: ' +
            str(self['wind']) + ' Rain per m^2:' + str(self['rain']))

# ====================================================================================================
