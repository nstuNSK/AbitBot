from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .db import configure

# Create your views here.
def index(request):
    if request.method == "POST":
        print("here")
        configure()
        return HttpResponse("eboy")
    else:
        return HttpResponse("no boy")
        
