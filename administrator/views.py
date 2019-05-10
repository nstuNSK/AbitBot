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

from AbitBot import settings
from .serializers import UserSerializer, NewsSerializer
from .models import *
from .db import configure, create_msgs, create_test

def getJWT(user):
    payload = jwt_payload_handler(user)
    return jwt.encode(payload, settings.SECRET_KEY)

def index(request):
    if request.method == "POST":
        configure()
        create_msgs()
        create_test()
        return Response(status = status.HTTP_204_NO_CONTENT)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        data = request.data
        if "login" in data and "password" in data:
            try:
                user = User.objects.get(login = data["login"])  
                if user.check_password(data["password"]):
                    jwt = getJWT(user)
                    serializer = UserSerializer(user)
                    res = {"jwt": jwt}
                    res.update(serializer.data)
                    return Response(data = res, status = status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status = status.HTTP_400_BAD_REQUEST)



class TestView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    serializer_class = UserSerializer

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(data = user.data, status = status.HTTP_200_OK)

class NewsList(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request):
        news = News.objects.all()
        res = []
        for item in news:
            res.append(NewsSerializer(item).data)
        return Response(data = res, status = status.HTTP_200_OK)

class NewsView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request):
        if "id" in request.GET:
            id = request.GET["id"]
            try:
                news = News.objects.get(id=id)
                res = NewsSerializer(news).data
                return Response(data = res, status = status.HTTP_200_OK)
            except:
                return Response(data = {"error": "Новость не найдена"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data = request.data
        if "id" in data:
            try:
                res = NewsSerializer(data)
                res.is_valid()
                res.save()
                return Response(data = res.data, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Что-то пошло не так"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        data = request.data
        if "id" in data:
            try:
                news = News.objects.get(id=data["id"])
                res = NewsSerializer(news, data)
                res.is_valid()
                res.save()
                return Response(data = res.data, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Новость не найдена"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        data = request.data
        if "id" in data:
            id = data["id"]
            news = News.objects.get(id=id)
            news.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

class NewsPublic(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if "id" in request.GET:
            id = request.GET["id"]
            news = News.objects.get(id=id)
            news.active = True
            news.save()
            # в after response сделать рассылку новости
            return Response(status = status.HTTP_204_NO_CONTENT)

class TestList(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request):
        Tests = Test.objects.all()
        res = []
        for item in Tests:
            res.append(TestSerializer(item).data)
        return Response(data = res, status = status.HTTP_200_OK)

class TestView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request):
        if "id" in request.GET:
            id = request.GET["id"]
            try:
                test = Test.objects.get(id=id)
                res = TestSerializer(test).data
                return Response(data = res, status = status.HTTP_200_OK)
            except:
                return Response(data = {"error": "Тест не найден"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        data = request.data
        if "id" in data:
            try:
                res = TestSerializer(data)
                res.is_valid()
                res.save()
                return Response(data = res.data, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Что-то пошло не так"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        data = request.data
        if "id" in data:
            try:
                test = Test.objects.get(id=data["id"])
                res = TestSerializer(test, data)
                res.is_valid()
                res.save()
                return Response(data = res.data, status = status.HTTP_200_OK)
            else:
                return Response(data = {"error": "Тест не найден"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        data = request.data
        if "id" in data:
            id = data["id"]
            test = Tests.objects.get(id=id)
            test.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(data = {"error": "Отсутствуют нужные поля"}, status = status.HTTP_400_BAD_REQUEST)

class TestPublic(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if "id" in request.GET:
            id = request.GET["id"]
            test = Test.objects.get(id=id)
            test.active = True
            test.save()
            return Response(status = status.HTTP_204_NO_CONTENT)