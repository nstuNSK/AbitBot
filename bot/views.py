from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

secretKey = "ewkncejknjkehjckwencwekjh"
accesString = "ce2190bb"
groupId = 172501053
# Create your views here.
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        if data["secret"] == secretKey:
            if data["type"] == 'confirmation' and data["group_id"] == groupId:
                return HttpResponse(accesString)
    #         elif data["type"] == "message_new":
    #             pass
    #             """врубаем бота"""
    #         elif:
    #             return 
    #     else:
    #         return 
    # else:
    #     return 
            