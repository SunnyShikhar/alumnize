from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import math
import numpy as nm
from numpy import array
from geopy.geocoders import Nominatim
from geotext import GeoText
from django.contrib import messages
from datetime import datetime
from almabase.tasks import beginTransform


def form(request):
    return render(request, "finalpage.html")

def home(request):
    return render(request, "index.html")

def loading(request):
    return render(request, "loading.html")

def upload(request):

    almaInput = []

    for eachFile in request.FILES.getlist("files"):
        almaInput.append(pd.read_csv(eachFile))

    masterFile = [pd.read_csv(request.FILES.getlist("master")[0])]
    request.close()

    return beginTransform(almaInput, masterFile)

    # if request.POST and request.FILES:
    #     print(request)
    #     print(request.POST)
    #     print(request.FILES)
    #     print(request.FILES.getlist("files"))
    #     print(request.FILES.getlist("master"))
        
    #     almaInput = []
        
    #     for eachFile in request.FILES.getlist("files"):
    #         almaInput.append(pd.read_csv(eachFile))

    #     masterFile = [pd.read_csv(request.FILES.getlist("master")[0])]
    #     request.close()

    #     return beginTransform(almaInput, masterFile)
    # else:
    #     return render(request,"error.html")         