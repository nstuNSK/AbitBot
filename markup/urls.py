from django.urls import path, include
from markup.views import *

urlpatterns = [
    path('', index),
    path('add_class/', Class_Add.as_view()),
    path('get_sample/', Get_Questions.as_view()),
    path('login/', LoginView.as_view()),
    path('db/', SecretDB.as_view())
]