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


class TaskSearchForm(forms.Form):
    name = forms.CharField(max_length=128,
                           label="Task name",
                           required=False)


class WorkerSearchForm(forms.Form):
    username = forms.CharField(max_length=128,
                               label="Username",
                               required=False)
