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
from .serializers import UserSerializer
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