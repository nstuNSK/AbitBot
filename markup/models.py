from django.db import models
from administrator.models import User

class Question(models.Model):
    """Вопрос для разметки"""

    question = models.TextField(verbose_name="Текст вопроса")
    answer = models.TextField(verbose_name="Ответ на вопрос")
    # isAvailable = models.BooleanField(verbose_name="Доступен") Is it need!?

    class Meta:
        verbose_name = "Вопрос для разметки"
        verbose_name_plural = "Вопросы для разметки"

class Mark(models.Model):
    """Класс для разметки"""

    id = models.IntegerField(verbose_name='id', primary_key=True)
    name = moedls.CharField(max_length=100, verbose_name="Название класса", unique=True)

    class Meta:
        verbose_name = "Класс для разметки"
        verbose_name_plural = "Классы для разметки"

class User_Question(models.Model):
    """Связующая между пользователем и вопросом"""

    user = models.ForeignKey(User, related_name='questions', verbose_name="Пользователь")
    question = models.ForeignKey(Question, related_name='mark_questions', verbose_name="Вопрос")
    mark = models.ForeignKey(Mark, related_name='questions', verbose_name="Метка класса")

class Question_Mark(models.Model):
    """Связующая между вопросом и меткой класса"""

    question = models.ForeignKey(Question, related_name='to_mark', verbose_name="Вопрос")
    mark = models.ForeignKey(Mark, related_name='marks_questions', verbose_name="Класс")



