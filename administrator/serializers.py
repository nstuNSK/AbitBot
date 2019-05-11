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

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
            "id",
            "answer",
            "reaction",
            "is_true"
        )

    def create(self, validate_data):
        return Answer.objects.create(**validate_data)

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "answers"
        )

    def create(self, validate_data):
        data = []
        answers = validate_data.get("answers")
        validate_data.pop("answers")
        question = Question.objects.create(**validate_data)
        for item in answers:
            serializer = AnswerSerializer(item)
            serializer.is_valid()
            serializer.save()
            question.add(serializer)
        return question

class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "updated_date",
            "start_date",
            "questions",
            "active"
        )

    def create(self, validate_data):

        data = []
        questions = validate_data.get("questions")
        validate_data.pop("questions")
        tets = Test.objects.create(**validate_data)
        for item in questions:
            serializer = QuestionsSerializer(item)
            serializer.is_valid()
            serializer.save()
            test.add(serializer)
        return test