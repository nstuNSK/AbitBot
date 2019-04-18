from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .db import configure, create_msgs

# Create your views here.
def index(request):
    if request.method == "POST":
        configure()
        create_msgs()
        return HttpResponse("eboy")
    else:
        return HttpResponse("no boy")
