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
    name = models.CharField(max_length=100, verbose_name="Название класса", unique=True)
    priority = models.IntegerField(verbose_name='Приоритет', default=1)

    class Meta:
        verbose_name = "Класс для разметки"
        verbose_name_plural = "Классы для разметки"

class User_Question(models.Model):
    """Связующая между пользователем и вопросом"""

    user = models.ForeignKey(User, related_name='questions', verbose_name="Пользователь", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='mark_questions', verbose_name="Вопрос", on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, related_name='questions', verbose_name="Метка класса", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "question"),)
class Question_Mark(models.Model):
    """Связующая между вопросом и меткой класса"""

    question = models.ForeignKey(Question, related_name='to_mark', verbose_name="Вопрос", on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, related_name='marks_questions', verbose_name="Класс", on_delete=models.CASCADE)
