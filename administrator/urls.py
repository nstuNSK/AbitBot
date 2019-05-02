from django.urls import path, include
from administrator.views import *

urlpatterns = [
    path('', index),
    path('login/', LoginView.as_view()),
    path('test/', TestView.as_view())
]