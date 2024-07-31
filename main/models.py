from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='study_groups')
    study_topic = models.CharField(max_length=255)
    study_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room_number = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class StudyGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    begin_date = models.DateField()
    target_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.goal

class StudyHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(StudyGoal, on_delete=models.CASCADE, null=True, blank=True)
    group_name = models.CharField(max_length=255, blank=True)
    completed_on = models.DateTimeField()
    details = models.TextField()

    def __str__(self):
        return f"{self.goal} completed on {self.completed_on}"
