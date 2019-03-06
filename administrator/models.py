from django.db import models

class Sphere(models.Model):
    """Сфера"""
    
    name = models.CharField(max_length = 100, verbose_name = "Название")

    class Meta:
        verbose_name        = "Сфера"
        verbose_name_plural = "Сферы"


class Subject(models.Model):
    """Предмет"""

    name = models.CharField(max_length = 100, verbose_name = "Название")

    class Meta:
        verbose_name        = "Предмет"
        verbose_name_plural = "Предметы"

class Direction(models.Model):
    """Направления"""
    id              = models.IntegerField(primary_key=True)
    name            = models.CharField(max_length = 50, verbose_name = "Название")
    faculty         = models.CharField(max_length = 150, verbose_name = "Факультет")
    keys_plus       = models.CharField(max_length = 15, verbose_name = "Код направления")
    ball_k          = models.IntegerField(verbose_name="Минимальный балл на контракт", null = True)
    ball_b          = models.IntegerField(verbose_name="Минимальный балл на бюджет", null = True)
    url             = models.URLField(verbose_name="Ссылка на направление")
    active          = models.BooleanField(default=True, verbose_name="Активно")
    description     = models.TextField(verbose_name="Описание", null = True)
    profile_name    = models.CharField(max_length = 50, verbose_name = "Профиль", null = True)
    spheres         = models.ManyToManyField(Sphere, verbose_name = "Сферы", related_name= "direction", blank = True)
    subjects        = models.ManyToManyField(Subject, verbose_name = "Предметы", related_name= "direction", blank = True)

    class Meta:
        verbose_name        = "Направление"
        verbose_name_plural = "Направления"

class Account(models.Model):
    """Аккаунт пользователя"""

    id              = models.IntegerField(verbose_name="id", primary_key=True)
    lk_code         = models.IntegerField(verbose_name="Код личного кабинета")
    subscribe       = models.BooleanField(default=False, verbose_name="Подписка")
    last_news       = models.CharField(max_length = 100, verbose_name = "Последняя новость")
    spheres         = models.ManyToManyField(Sphere, verbose_name = "Сферы", related_name= "account", blank = True)
    subjects        = models.ManyToManyField(Subject, verbose_name = "Предметы", related_name= "account", blank = True)

    class Meta:
        verbose_name        = "Пользователь"
        verbose_name_plural = "Пользователи"

class Msg(models.Model):
    """Сообщение"""

    pay = models.CharField(max_length = 50, verbose_name = "payload")
    msg = models.TextField(verbose_name="Сообщение")
    
    class Meta:
        verbose_name        = "Сообщение"
        verbose_name_plural = "Сообщения"

class Answer(models.Model):
    """Ответ"""

    answer      = models.TextField(verbose_name="Ответ")
    reaction    = models.TextField(verbose_name="Реакция на ответ")
    is_true     = models.BooleanField(verbose_name="Верный ответ")

    class Meta:
        verbose_name        = "Ответ"
        verbose_name_plural = "Ответы"



class Question(models.Model):
    """Вопрос"""

    question    = models.TextField(verbose_name="Вопрос")
    answers     = models.ForeignKey(Answer, on_delete = models.CASCADE, verbose_name = "Ответы", related_name="question")

    class Meta:
        verbose_name        = "Вопрос"
        verbose_name_plural = "Вопросы"

class Test(models.Model):
    """Тест"""

    name            = models.CharField(max_length = 50, verbose_name = "Название")
    updated_date    = models.DateTimeField(verbose_name = "Дата и время изменения", auto_now = True)
    start_date      = models.DateField(verbose_name="Дата начала теста")
    questions       = models.ManyToManyField(Question, verbose_name = "Вопросы", related_name="test", blank = True)

    class Meta:
        verbose_name        = "Тест"
        verbose_name_plural = "Тесты"