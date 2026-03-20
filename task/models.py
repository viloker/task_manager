from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    PRIORITY_CHOICE_LIST = [
        ("Urgent", "urgent"),
        ("High", "high")
    ]
    name = models.CharField(max_length=128)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICE_LIST)
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True)
    assignees = models.ManyToManyField("Worker", related_name="tasks")

    def __str__(self) -> str:
        return f"{self.name}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        related_name="workers",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.username}: ({self.position})"


class Position(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.name}"
