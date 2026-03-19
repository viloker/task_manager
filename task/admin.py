from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, TaskType, Worker, Position


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ...


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)


admin.site.register(TaskType)
admin.site.register(Position)
