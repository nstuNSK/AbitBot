from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.staticfiles import finders

from AbitBot import settings
import pandas as pd

import random


class Class_Add(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    # authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)


    def add_class(self, num, id, df):
        df.loc[id-1, 'classes'] += str(num)+" "
    
    def add_classes(self, objs):
        # results = finders.find('files/q.csv')
        df = pd.read_csv("/home/Main/AbitBot/static/files/q.csv", encoding='utf8', delimiter=";")
        for obj in objs:
            self.add_class(obj['type'], obj['id'], df)

    
    def post(self, request):
        data = request.data
        if mas in data:
            questions = data['mas']
            try:
                self.add_classes(questions)
                res = {"status": "success", "status_code": "200"}
                return Response(data = res, status = status.HTTP_200_OK)
            except:
                res = {"status": "failed", "status_code": "400"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

class Get_Questions(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    # authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def get_q(self):
        # results = finders.find('files/q.csv')
        df = pd.read_csv("/home/Main/AbitBot/static/files/q.csv", encoding='utf8', delimiter=";")
        available_q = df[df['count']<3]
        if len(available_q) % 10 == 0:
            count_of_samples = len(available_q)/10
        else:
            count_of_samples = int(len(available_q)/10)+1
        num_sample = random.randint(0, count_of_samples)
        if num_sample != count_of_samples:
            sample = available_q[10*num_sample:10*num_sample+10]
        else:
            last_index = len(available_q)-1
            sample = available_q[10*num_sample:last_index]
        return sample.values

    def convert_to_json(self, sample):
        result = {"questions": []}
        for s in sample:
            result["questions"].append({"id": s[0], "question": s[1]})
        return result


    def post(self, request):
        sample = self.get_q()
        result = self.convert_to_json(sample)
        return Response(data = res, status = status.HTTP_200_OK)


        
