from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from task.models import Tag, CustomUser, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email"
        )


class CustomuserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match. Please confirm your password.",
            )
        else:
            user = self.instance
            user_auth = authenticate(username=user.username, password=password)
            if user_auth is None:
                self.add_error(
                    "password",
                    "Please enter your password correctly",
                )

        return cleaned_data


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["tags"].queryset = Tag.objects.filter(owner=user)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ("name", "content", "deadline", "priority", "tags")

    def clean_deadline(self):
        if self.cleaned_data["deadline"]:
            if self.cleaned_data["deadline"] < timezone.now():
                raise ValidationError("Deadline can not be earlier than today")
            return self.cleaned_data["deadline"]
