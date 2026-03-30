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
from .forms import TaskForm, WorkerForm


@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_done_tasks = Task.objects.filter(is_completed=True).count()
    num_workers = Worker.objects.count()

    num_urgent_tasks = Task.objects.filter(priority="Urgent", is_completed=False).count()

    last_completed_tasks = Task.objects.filter(is_completed=True).order_by("-deadline")[:5]

    context = {
        "num_tasks": num_tasks,
        "num_done_tasks": num_done_tasks,
        "num_workers": num_workers,
        "num_urgent_tasks": num_urgent_tasks,
        "last_completed_tasks": last_completed_tasks
    }

    return render(
        request,
        "task/index.html",
        context=context)


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
    model = Worker
    template_name = "task/worker_list.html"
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    template_name = "task/worker_create.html"
    success_url = reverse_lazy("task:worker-list")
    form_class = WorkerForm


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    template_name = "task/worker_create.html"
    success_url = reverse_lazy("task:worker-list")
    form_class = WorkerForm


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")
    template_name = "task/worker_delete.html"
