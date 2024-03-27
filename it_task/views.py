from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from it_task.forms import TaskTypeSearchForm, PositionSearchForm, WorkerCreationForm, TaskForm, TaskSearchForm
from it_task.models import Task, TaskType, Position, Worker


def index(request):
    return render(request, "it_task/index.html")


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


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm()
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(task_type_id=self.kwargs['pk'])
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            qs = qs.filter(name__icontains=form.cleaned_data["name"])
        return qs





class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        task_id = self.object.id
        return reverse_lazy("task-detail", kwargs={"pk": task_id})


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        task_id = self.object.id
        return reverse_lazy("task-detail", kwargs={"pk": task_id})


class TaskDetailView(generic.DetailView):
    model = Task
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['assigned_workers'] = task.assignees.all()
        return context


class TaskDeleteView(generic.DeleteView):
    model = Task

    def get_success_url(self):
        task_type_id = self.object.task_type.id
        return reverse_lazy("task-list", kwargs={"pk": task_type_id})


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 10


class WorkerCreateView(generic.CreateView):
    model = Worker
    success_url = reverse_lazy("worker-list")
    form_class = WorkerCreationForm


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("worker-list")