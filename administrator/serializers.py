from rest_framework import serializers
from .models import User

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