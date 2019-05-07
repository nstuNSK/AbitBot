from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "login",
            "password",
            "date_joined",
            "firstName",
            "lastName",
        )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 5

#class TestSerializer(serializers.ModelSerializer):

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = (
            "id",
            "name",
            "description",
            "active"
        )

    def create(self,validate_data):
        return News.objects.create(**validate_data)