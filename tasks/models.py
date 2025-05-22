from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ("New", "New"),
    ("In Progress", "In Progress"),
    ("Pending", "Pending"),
    ("Blocked", "Blocked"),
    ("Done", "Done"),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        unique_together = ("name",)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="New")
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ("-created_at",)
        verbose_name = "SubTask"
        unique_together = ("title", "task")

    def __str__(self):
        return self.title












