from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import Task, Worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class WorkerForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + ("position", )


class TaskSearchForm(forms.Form):
    name = forms.CharField(max_length=128,
                           label="Task name",
                           required=False)


class WorkerSearchForm(forms.Form):
    username = forms.CharField(max_length=128,
                               label="Username",
                               required=False)


class PositionSearchForm(forms.Form):
    name = forms.CharField(max_length=128,
                           label="Position name",
                           required=False)
