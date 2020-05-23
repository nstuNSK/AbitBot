from django.db import models

class Scenario(models.Model):
    """Сценарий"""

    question        = models.TextField(verbose_name="Вспомогательный вопрос")
    answer          = models.TextField(verbose_name="Ответ", default="-")
    positive        = models.TextField(verbose_name="Реакция на положительный ответ")
    negative        = models.TextField(verbose_name="Реакция на отрицательный ответ")

    class Meta:
        verbose_name        = "Сценарий"
        verbose_name_plural = "Сценарии"


class Keyword(models.Model):
    """Ключевое слово"""

    word = models.CharField(max_length = 100, verbose_name = "Слово")
    scenario = models.ForeignKey(Scenario, verbose_name = "Сценарий", on_delete = models.CASCADE) 

    class Meta:
        verbose_name        = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"