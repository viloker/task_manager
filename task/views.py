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


@login_required
def index(request):
    return render(request, "task/index.html")


class TaskListView(LoginRequiredMixin, ListView):
    ...


class TaskDetailView(LoginRequiredMixin, DetailView):
    ...


class TaskCreateView(LoginRequiredMixin, CreateView):
    ...


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    ...


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    ...
