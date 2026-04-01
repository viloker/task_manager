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

from django.db.models import Count
from .models import Task, Worker, Position
from .forms import TaskForm, WorkerForm, TaskSearchForm, WorkerSearchForm, PositionSearchForm


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


class MyTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task/my_task.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = TaskSearchForm(self.request.GET, None)

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(assignees=user)
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = TaskSearchForm(self.request.GET, None)
        context["priority_list"] = Task.PRIORITY_CHOICE_LIST
        print(self.request.GET)
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        priority = self.request.GET.get("priority", None)
        is_completed = self.request.GET.get("is_completed", None)

        queryset = super().get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if priority:
            queryset = queryset.filter(priority=priority)

        if is_completed:
            queryset = queryset.filter(is_completed=is_completed)

        return queryset


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task

    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = WorkerSearchForm(self.request.GET, None)

        return context

    def get_queryset(self):
        queryset = self.model.objects.select_related("position")

        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset


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


class PositionListView(LoginRequiredMixin, ListView):
    model = Position

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["count_workers"] = self.get_queryset()
        context["search"] = PositionSearchForm(self.request.GET, None)

        return context

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = self.model.objects.annotate(count_workers=Count("workers"))
        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("task:position-list")
    template_name = "task/position_delete.html"
