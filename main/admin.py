# admin.py
from django.contrib import admin
from .models import StudyGroup, StudyGoal, StudyHistory

admin.site.register(StudyGroup)
admin.site.register(StudyGoal)
admin.site.register(StudyHistory)
