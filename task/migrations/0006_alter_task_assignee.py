# Generated by Django 4.2.7 on 2023-11-27 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0005_remove_task_assignees_task_assignee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="assignee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
