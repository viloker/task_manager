from django import forms

from .models import Task, Worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["username", "password"]
