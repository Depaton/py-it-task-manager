from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from it_task.forms import TaskTypeSearchForm, PositionSearchForm, WorkerCreationForm, TaskForm, TaskSearchForm, \
    WorkerSearchForm
from it_task.models import Task, TaskType, Position, Worker


@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers
    }
    return render(request, "it_task/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
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


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm()
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            qs = self.model.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        else:
            qs = self.model.objects.all()
        return qs


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("position-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm()
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.filter(task_type_id=self.kwargs["pk"])
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            qs = qs.filter(name__icontains=form.cleaned_data["name"])
        return qs


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        task_id = self.object.id
        return reverse_lazy("task-detail", kwargs={"pk": task_id})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        task_id = self.object.id
        return reverse_lazy("task-detail", kwargs={"pk": task_id})


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['assigned_workers'] = task.assignees.all()
        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task

    def get_success_url(self):
        task_type_id = self.object.task_type.id
        return reverse_lazy("task-list", kwargs={"pk": task_type_id})


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm()
        return context

    def get_queryset(self, **kwargs):
        qs = super(WorkerListView, self).get_queryset(**kwargs)
        if 'pk' in self.kwargs and self.kwargs['pk']:
            qs = qs.filter(position_id=self.kwargs["pk"])
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            last_name = form.cleaned_data.get("last_name")
            if last_name:
                qs = qs.filter(last_name__icontains=last_name)
        return qs


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    success_url = reverse_lazy("worker-list")
    form_class = WorkerCreationForm


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("worker-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.object
        tasks = Task.objects.filter(assignees=worker)
        context['tasks'] = tasks
        return context
