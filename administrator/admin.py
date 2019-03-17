from django.contrib import admin
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lk_code",
        "subscribe",
        "last_news",
    )
admin.site.register(Account, AccountAdmin)

class DirectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "faculty",
        "keys_plus",
        "ball_k",
        "ball_b",
        "url",
        "active",
        "description",
        "profile_name",
    )
admin.site.register(Direction, DirectionAdmin)

class MsgAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "pay",
        "msg"
    )

admin.site.register(Msg, MsgAdmin)

class SphereAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

admin.site.register(Sphere, SphereAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

admin.site.register(Subject, SubjectAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "answer",
        "reaction",
        "is_true"
    )

admin.site.register(Answer, AnswerAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question"
    )

admin.site.register(Question, QuestionAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "updated_date",
        "start_date"
    )

admin.site.register(Test, TestAdmin)