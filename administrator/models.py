from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):

    def _create_user(self, login, password, **extra_fields):
        """
        Creates and saves a User with the given login,and password.
        """
        if not login:
            raise ValueError('The given login must be set')
        try:
            with transaction.atomic():
                user = self.model(login=login, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(login, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""

    firstName       = models.CharField(max_length = 50, verbose_name = "Имя", default = "name")
    lastName        = models.CharField(max_length = 50, verbose_name = "Фамилия", default = "surname")
    login           = models.CharField(max_length = 50, verbose_name = "Логин", unique = True)
    password        = models.TextField(verbose_name = "Пароль", default = "pass")

    is_active       = models.BooleanField(default=True, verbose_name="Аккаунт действует")
    is_staff        = models.BooleanField(default=False, verbose_name="Сотрудник")
    date_joined     = models.DateTimeField(default=timezone.now)

    objects         = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['password', "firstName", "lastName"]

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return "{} {} id{}".format(self.firstName, self.lastName, str(self.id))

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

# class User(models.Model):
#      """Модель пользователя"""
#      login           = models.CharField(max_length = 50, verbose_name = "Логин", unique = True)

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
    RN              = models.IntegerField(verbose_name="Приоритет", null = True)

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

class News(models.Model):
    """Новости"""

    name            = models.CharField(max_length = 50, verbose_name = "Название")
    description     = models.TextField(verbose_name = "Описание")
    active          = models.BooleanField(verbose_name = "Активный", default = False)

    class Meta:
        verbose_name        = "Новость"
        verbose_name_plural = "Новости"

class Account(models.Model):
    """Аккаунт пользователя"""

    id                  = models.IntegerField(verbose_name="id", primary_key = True)
    random_id           = models.IntegerField(verbose_name="идентификатор сообщений", default = 0 )
    lk_code             = models.IntegerField(verbose_name="Код личного кабинета", default = 0)
    state               = models.BooleanField(verbose_name="Состояние", default = False)
    currency_snap_id    = models.IntegerField(verbose_name="Текущий снимок", default= -1)
    subscribe           = models.BooleanField(default=False, verbose_name ="Подписка")
    last_news           = models.CharField(max_length = 100, verbose_name = "Последняя новость", default = "null")
    spheres             = models.ManyToManyField(Sphere, verbose_name = "Сферы", related_name= "account", blank = True)
    subjects            = models.ManyToManyField(Subject, verbose_name = "Предметы", related_name= "account", blank = True)
    tests               = models.ManyToManyField(ResultOfTest, verbose_name = "Результаты пройденных тестов", related_name = "account")
    feedback            = models.CharField(max_length = 20, verbose_name = "Обратная связь", default = "false")

    class Meta:
        verbose_name        = "Пользователь"
        verbose_name_plural = "Пользователи"