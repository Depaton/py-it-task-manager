from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from it_task.models import Worker, Task


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Type"}
        )
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Position"}
        )
    )


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position",)


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "position",)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Старий пароль'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Новий пароль'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Підтвердження нового паролю'})


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Task Name"}
        )
    )


class WorkerSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by Last name"}
        )
    )
