from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)

from django.shortcuts import render

from .models import Task


@login_required
def index(request):
    return render(request, "task/index.html")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task/task_list.html"
    paginate_by = 10


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    ...


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    ...


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    ...
