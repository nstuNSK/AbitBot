from django.urls import path, include
from .views import *

urlpatterns = [
    path('', StatisticaView.as_view())
]