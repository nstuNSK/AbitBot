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
    idNSTU          = models.IntegerField(verbose_name = "id НГТУ", null = True)
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

class Msg(models.Model):
    """Сообщение"""

    pay = models.CharField(max_length = 50, verbose_name = "payload")
    msg = models.TextField(verbose_name="Сообщение")

    class Meta:
        verbose_name        = "Сообщение"
        verbose_name_plural = "Сообщения"

class Answer(models.Model):
    """Ответ"""

    answer      = models.CharField(max_length = 40 ,verbose_name="Ответ")
    reaction    = models.TextField(verbose_name="Реакция на ответ")
    is_true     = models.BooleanField(verbose_name="Верный ответ")

    def __str__(self):
        return "{} ({})".format(self.answer, self.is_true)
    class Meta:
        verbose_name        = "Ответ"
        verbose_name_plural = "Ответы"



class Question(models.Model):
    """Вопрос"""

    number      = models.IntegerField(verbose_name = "Номер вопроса", null = True)
    question    = models.TextField(verbose_name="Вопрос")
    answers     = models.ManyToManyField(Answer, verbose_name = "Ответы", related_name="question", blank = True)

    def __str__(self):
        return "{} {}".format(self.number, self.question)
    class Meta:
        verbose_name        = "Вопрос"
        verbose_name_plural = "Вопросы"

class Test(models.Model):
    """Тест"""

    name            = models.CharField(max_length = 50, verbose_name = "Название")
    updated_date    = models.DateTimeField(verbose_name = "Дата и время изменения", auto_now = True)
    start_date      = models.DateField(verbose_name="Дата начала теста")
    questions       = models.ManyToManyField(Question, verbose_name = "Вопросы", related_name="test", blank = True)
    active          = models.BooleanField(verbose_name = "Активный", default = False)

    class Meta:
        verbose_name        = "Тест"
        verbose_name_plural = "Тесты"

class ResultOfTest(models.Model):
    """Результат теста"""

    rightAnswer     = models.IntegerField(default = 0, verbose_name = "Количество правильных ответов")
    allAnswer       = models.IntegerField(default = 0, verbose_name = "Количество всех ответов")
    test            = models.ForeignKey(Test, on_delete = models.CASCADE,verbose_name = "Тест", related_name = "result")
    class Meta:
        verbose_name        = "Результат теста"
        verbose_name_plural = "Результаты теста"

class Account(models.Model):
    """Аккаунт пользователя"""

    id              = models.IntegerField(verbose_name="id", primary_key = True)
    random_id       = models.IntegerField(verbose_name="идентификатор сообщений", default = 0 )
    lk_code         = models.IntegerField(verbose_name="Код личного кабинета", default = 0)
    subscribe       = models.BooleanField(default=False, verbose_name ="Подписка")
    last_news       = models.CharField(max_length = 100, verbose_name = "Последняя новость", default = "null")
    spheres         = models.ManyToManyField(Sphere, verbose_name = "Сферы", related_name= "account", blank = True)
    subjects        = models.ManyToManyField(Subject, verbose_name = "Предметы", related_name= "account", blank = True)
    tests           = models.ManyToManyField(ResultOfTest, verbose_name = "Результаты пройденных тестов", related_name = "account")

    class Meta:
        verbose_name        = "Пользователь"
        verbose_name_plural = "Пользователи"