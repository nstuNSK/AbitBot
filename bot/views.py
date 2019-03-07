from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from . import bot

secretKey = "ewkncejknjkehjckwencwekjh"
accesString = "ce2190bb"
groupId = 172501053
# Create your views here.
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        if data["secret"] == secretKey:
            if data["group_id"] == groupId:
                if data["type"] == 'confirmation':
                    return HttpResponse(accesString)
                elif data["type"] == "message_new":
                    obj = data["object"]
                    if "payload" in obj:
                        bot.data_processing(id = obj["from_id"], pay = bytes(obj["payload"], 'cp1251').decode('utf-8'), msg = obj["text"])
                    else:
                        bot.data_processing(id = obj["from_id"], pay = " ", msg = obj["text"])
                #elif data["type"] == "group_join":

                #elif data["type"] == "group_leave":

                return HttpResponse("ok", status = 200)