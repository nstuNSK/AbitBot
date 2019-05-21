from django.urls import path, include
from administrator.views import *

urlpatterns = [
    path('', index),
    path('create/', createdb),
    path('login/', LoginView.as_view()),
    path('testView/', TestView.as_view()),
    path('tests/', TestList.as_view()),
    path('testPublic/', TestPublic.as_view()),
    path('news/', NewsList.as_view()),
    path('newsView/', NewsView.as_view()),
    path('public/', NewsPublic.as_view()),
]