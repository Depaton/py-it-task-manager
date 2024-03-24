"""
URL configuration for it_task_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from it_task.views import TaskTypeListView, TaskTypeCreateView, TaskTypeUpdateView, TaskTypeDeleteView, \
    PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView, TaskListView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView, WorkerListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("task-type-list/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-type-list/create", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-type-list/<int:pk>/update", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-type-list/<int:pk>/delete", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("position-list/", PositionListView.as_view(), name="position-list"),
    path("position-list/create", PositionCreateView.as_view(), name="position-create"),
    path("position-list/<int:pk>/update", PositionUpdateView.as_view(), name="position-update"),
    path("position-list/<int:pk>/delete", PositionDeleteView.as_view(), name="position-delete"),
    path("task-list/<int:pk>", TaskListView.as_view(), name="task-list"),
    path("task-list/create", TaskCreateView.as_view(), name="task-create"),
    path("task-list/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("task-list/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
    path("worker-list/", WorkerListView.as_view(), name="task-delete")
]
