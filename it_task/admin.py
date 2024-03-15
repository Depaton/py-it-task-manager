from django.contrib import admin

from it_task.models import Worker, TaskType, Task, Position

admin.site.register(Worker)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Position)
