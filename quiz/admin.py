from django.contrib import admin
from .models import Topic, Question, Answer,UserRecord

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserRecord)