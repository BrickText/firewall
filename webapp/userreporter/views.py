from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

class MapView(View):

    def get(self, request):
        return render(request, 'index.html',  locals())



