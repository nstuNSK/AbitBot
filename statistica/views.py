from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from statistica.actions import *
from administrator.models import *


import requests
import csv
import json

class StatisticaView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request):
        # try:
            if request.query_params["action"]=="csv":
                upgrade_csv()
            elif request.query_params["action"]=="stat":
                stat = get_stat_from_csv()
                return Response(data=stat, status=status.HTTP_200_OK)

        #     return Response(status = status.HTTP_204_NO_CONTENT)
        # except:
        #     raise
        #     return Response(status = status.HTTP_400_BAD_REQUEST)
    

