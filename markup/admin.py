from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Mark)
admin.site.register(User_Question)
admin.site.register(Question_Mark)