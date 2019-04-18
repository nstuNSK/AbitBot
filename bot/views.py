from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from . import bot

secretKey1 = "ewkncejknjkehjckwencwekjh"
accesString1 = "ce2190bb"
groupId1 = 172501053

secretKey2 = "aefc6438516236415a8a7d55dff4206c"
accesString2 = "8c3d3379"
groupId2 = 181296685
# Create your views here.
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        
        if data["type"] == "message_new":
            obj = data["object"]
            if "payload" in obj:
                pay = obj["payload"][1:-1]
                try:
                    pay = bytes(pay, 'cp1251').decode('utf-8')
                except:
                    pass
                bot.data_processing(id = obj["from_id"], pay = pay, msg = obj["text"])
            else:
                bot.data_processing(id = obj["from_id"], pay = " ", msg = obj["text"])
                #elif data["type"] == "group_join":

                #elif data["type"] == "group_leave":
            return HttpResponse("ok", status = 200)
        elif data["secret"] == secretKey1 and data["group_id"] == groupId1 and data["type"] == 'confirmation':
            return HttpResponse(accesString1)
        elif data["secret"] == secretKey2 and data["group_id"] == groupId2 and data["type"] == 'confirmation':
            return HttpResponse(accesString2)
                