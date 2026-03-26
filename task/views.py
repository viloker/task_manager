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
from django.urls import reverse_lazy

from .models import Task, Worker
from .forms import TaskForm


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
    model = Task
    success_url = reverse_lazy("task:task-list")
    form_class = TaskForm
    template_name = "task/task_create.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = reverse_lazy("task:task-list")
    form_class = TaskForm
    template_name = "task/task_create.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")
    template_name = "task/task_delete.html"


class WorkerListView(LoginRequiredMixin, ListView):
    ...


class WorkerDetailView(LoginRequiredMixin, DetailView):
    ...


class WorkerCreateView(LoginRequiredMixin, CreateView):
    ...


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    ...