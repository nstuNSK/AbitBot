from django.urls import path, include
from markup.views import views

urlpatterns = [
    path('add_class/', Class_Add.as_view()),
    path('get_sample/', Get_Questions.as_view())
]