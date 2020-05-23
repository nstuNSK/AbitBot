from django.contrib import admin
from .models import *

class ScenarioAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "question",
        "positive",
        "negative"
    )

admin.site.register(Scenario, ScenarioAdmin)

class KeywordAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "word",
    )

admin.site.register(Keyword, KeywordAdmin)
