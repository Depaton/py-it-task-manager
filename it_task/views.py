from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from it_task.forms import TaskTypeSearchForm, PositionSearchForm
from it_task.models import Task, TaskType, Position


class TaskTypeListView(generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        context["search_form"] = TaskTypeSearchForm()
        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            queryset = self.model.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        else:
            queryset = self.model.objects.all()

        return queryset

class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task-type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task-type-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm()
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            queryset = self.model.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        else:
            queryset = self.model.objects.all()

        return queryset

class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("position-list")
