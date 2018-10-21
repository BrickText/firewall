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
from django.conf.urls.static import static
from django.conf import settings

from userreporter.views import get_map, post_confirm, get_fires,\
    post_predict_new_fire, populate_base_on_start

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_map),
    path('fire_confirm', post_confirm),
    path('get_fire', get_fires),
    path('predict_fire', post_predict_new_fire),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


populate_base_on_start()
