from django.urls import path

from task.views import (
    index,
    TagDeleteView,
    TagUpdateView,
    TagCreateView,
    TagListView,
    CustomUserDeleteView,
    CustomUserUpdateView,
    CustomUserDetailView,
    CustomUserCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskCreateView,
    TaskListView,
    change_task_status,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "tags/",
        TagListView.as_view(),
        name="tag-list",
    ),
    path(
        "tags/create/",
        TagCreateView.as_view(),
        name="tag-create",
    ),
    path(
        "tags/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update",
    ),
    path(
        "tags/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete",
    ),
    path(
        "customusers/create/",
        CustomUserCreateView.as_view(),
        name="customuser-create",
    ),
    path(
        "customusers/<int:pk>/",
        CustomUserDetailView.as_view(),
        name="customuser-detail"),
    path(
        "customusers/<int:pk>/update/",
        CustomUserUpdateView.as_view(),
        name="customuser-update",
    ),
    path(
        "customusers/<int:pk>/delete/",
        CustomUserDeleteView.as_view(),
        name="customuser-delete",
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="tasks-create",
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path(
        "tasks/<int:pk>/change-status/",
        change_task_status,
        name="change-task-status",
    ),
]

app_name = "task"
