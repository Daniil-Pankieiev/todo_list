from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from task.forms import (
    TagSearchForm,
    CustomUserCreationForm,
    CustomuserUpdateForm,
    TaskSearchForm,
    TaskForm,
)
from task.models import Task, Tag, CustomUser


def index(request):
    """View function for the home page of the site."""

    num_tags = Tag.objects.count()
    num_tasks = Task.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tags": num_tags,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task/index.html", context=context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TagSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Tag.objects.filter(owner=user)
        form = TagSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ["name"]
    success_url = reverse_lazy("task:tag-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = ["name"]
    success_url = reverse_lazy("task:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task:tag-list")


class CustomUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser


class CustomUserCreateView(generic.CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("task:index")


class CustomUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomuserUpdateForm

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]

        if password:
            user.set_password(password)

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("task:customuser-detail", kwargs={"pk": self.object.pk})


class CustomUserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CustomUser
    success_url = reverse_lazy("task:index")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(assignee=user)
        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")

    def form_valid(self, form):
        form.instance.assignee = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


def change_task_status(request, pk) -> HttpResponseRedirect:
    task = Task.objects.get(id=pk)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(reverse_lazy("task:task-list"))
