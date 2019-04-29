from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .db import configure, create_msgs, create_test
import json

# Create your views here.
def index(request):
    if request.method == "POST":
        configure()
        create_msgs()
        create_test()
        return HttpResponse("ok")
    else:
        return HttpResponse("no ok")


# '''Аунтификация'''
# def login(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode("utf-8"))
#         if "login" in data and "password" in data:
#             if data["login"] = "admin" and data["password"] = "pasbot2018":
#                 return HttpResponse("ok")
#             else:
#                 return HttpResponse("no ok")
#         else:
#             return HttpResponse("no ok")
#     else:
#         return HttpResponse("no ok")


# '''Новости'''
# def newsList(request):
#     if request.method == "GET":
#         pass

# def newsDelete(request):
#     pass

# def newsUpdate(request):
#     pass

# def newsSend(request):
#     pass

# def newsAdd(request):
#     pass

# '''Тестирование'''
# def testsList(request):
#     pass

# def testDelete(request):
#     pass

# def testUpdate(request):
#     pass

# def testSend(request):
#     pass

# def testAdd(request):
#     pass


# '''Статистика'''
# def stat(request):
#     pass