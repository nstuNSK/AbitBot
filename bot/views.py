from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from . import bot

#secretKey = "ewkncejknjkehjckwencwekjh"
#accesString = "ce2190bb"
#groupId = 172501053

secretKey = "aefc6438516236415a8a7d55dff4206c"
accesString = "8c3d3379"
groupId = 181296685
# Create your views here.
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        
        if data["type"] == "message_new":
            obj = data["object"]

            if obj["form_id"] != "176468928":
                bot.data_processing(id = obj["from_id"], pay = "engineering_works", msg = obj["text"])
                return HttpResponse("ok", status = 200)

            if "payload" in obj:
                pay = obj["payload"][1:-1]
                try:
                    pay = bytes(pay, 'cp1251').decode('utf-8')
                except:
                    pass
                bot.data_processing(id = obj["from_id"], pay = pay, msg = obj["text"])
            else:
                bot.data_processing(id = obj["from_id"], pay = " ", msg = obj["text"])
            return HttpResponse("ok", status = 200)

        elif data["secret"] == secretKey and data["group_id"] == groupId and data["type"] == 'confirmation':
            return HttpResponse(accesString2)
                