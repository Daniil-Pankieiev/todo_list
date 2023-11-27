from django.db import models
from django.contrib.auth.models import AbstractUser

from todo_list.settings import AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class CustomUser(AbstractUser):

    class Meta:
        verbose_name = "customuser"
        verbose_name_plural = "customusers"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )
    STATUS_CHOICES = (
        ("In progress", "In progress"),
        ("Completed on time", "Completed on time"),
        ("Completed after the deadline", "Completed after the deadline"),
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="In progress",
    )
    content = models.TextField()
    deadline = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="LOW",
    )
    tag = models.ManyToManyField(Tag, related_name="tasks")
    assignees = models.ManyToManyField(AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.name
