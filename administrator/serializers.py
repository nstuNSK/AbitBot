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
            "isAdmin",
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
    answers = AnswerSerializer(many=True)
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
            serializer = AnswerSerializer(data=item)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            answer = Answer.objects.get(id = serializer.data["id"])
            question.answers.add(answer)
        return question

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "questions",
            "active"
        )

    def create(self, validate_data):

        data = []
        if "questions" in validate_data:
            questions = validate_data.get("questions")
            validate_data.pop("questions")
        else:
            questions = []
        test = Test.objects.create(**validate_data)
        for item in questions:
            serializer = QuestionSerializer(data=item)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            question = Question.objects.get(id=serializer.data["id"])
            test.questions.add(question)
        return test