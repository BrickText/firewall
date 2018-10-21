"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userreporter.views import get_map, post_confirm, get_fires, post_predict_new_fire
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_map),
    path('fire_confirm', post_confirm),
    path('get_fire', get_fires),
    path('predict_fire', post_predict_new_fire),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

def populate_base_on_start():
    with open('../models/fire_clustering.b', 'rb') as f:
        fire_clustering = pickle.load(f)
    centroids = fire_clustering.cluster_centers_
    df = pd.DataFrame(
        [get_features(centroid[0], centroid[1]).to_pandas()
         for centroid in centroids])
    with open('../models/svm.b', 'rb') as f:
        svm = pickle.load(f)
    print([get_features(centroid[0], centroid[1]).to_pandas()
         for centroid in centroids])
    area = svm.predict(df)
    area = np.exp(area) * 10000
    
    concatenatedData = np.concatenate((centroids, np.reshape(area.T, (-1, 1))), axis=1)
    dbObjects = []
    
    for entry in concatenatedData:
        dbObjects.append(Fire(lat=entry[0], lng=entry[1], range=entry[2], is_active=False))
    Fire.objects.bulk_create(dbObjects)


populate_base_on_start()