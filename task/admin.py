from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task, Tag, CustomUser


@admin.register(CustomUser)
class WorkerAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = (
        "is_completed",
        "assignee",
        "tags",
        "priority",
        "deadline",
    )
    list_display = (
        "name",
        "is_completed",
        "created_at",
        "content",
        "deadline",
        "priority",
        "assignee",
        "all_tags",
    )

    def all_tags(self, task):
        return ", ".join([tag.name for tag in task.tags.all()])

    all_tags.short_description = "tags"


@admin.register(Tag)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "owner"
    )
