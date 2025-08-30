# Create your models here.

from django.db import models
from django.conf import settings
from users.models import User

class Task(models.Model):
    class Status(models.TextChoices):
        TO_DO = 'TO_DO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.TO_DO
    )
    total_minutes = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User, 
        related_name='created_tasks', 
        on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        User, 
        related_name='assigned_tasks', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

