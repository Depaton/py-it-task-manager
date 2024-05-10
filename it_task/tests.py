import unittest

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from django import forms

from it_task.forms import TaskSearchForm, WorkerSearchForm, TaskTypeSearchForm, PositionSearchForm, WorkerCreationForm, \
    WorkerUpdateForm, CustomPasswordChangeForm
from it_task.models import TaskType, Position, Task, Worker

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = User.objects.create_user(username="test_user", password="12345")
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Fix bug",
            description="Fix the critical bug in the system",
            deadline="2024-01-01",
            is_completed=False,
            priority="High",
            task_type=self.task_type
        )
        self.task.assignees.add(self.worker)

    def test_task_type_str(self):
        task_type = TaskType.objects.get(name="Bug")
        self.assertEqual(str(task_type), "Bug")

    def test_position_str(self):
        position = Position.objects.get(name="Developer")
        self.assertEqual(str(position), "Developer")

    def test_worker_str(self):
        user = User.objects.get(username="test_user")
        expected_str = f"{user.position} - {user.first_name} {user.last_name}"
        self.assertEqual(str(user), expected_str)

    def test_task_str(self):
        task = Task.objects.get(name="Fix bug")
        expected_str = f"{task.name} ({task.task_type}): {task.description}"
        self.assertEqual(str(task), expected_str)

    def test_task_assignees(self):
        task = Task.objects.get(name="Fix bug")
        self.assertIn(self.worker, task.assignees.all())

    class TestSearchForms(unittest.TestCase):
        def test_task_search_form(self):
            form = TaskSearchForm()
            self.assertIsInstance(form.fields['name'], forms.CharField)
            self.assertEqual(form.fields['name'].max_length, 255)
            self.assertFalse(form.fields['name'].required)
            self.assertEqual(form.fields['name'].label, '')
            self.assertIsInstance(form.fields['name'].widget, forms.TextInput)
            self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Search by Task Name')

        def test_worker_search_form(self):
            form = WorkerSearchForm()
            self.assertIsInstance(form.fields['last_name'], forms.CharField)
            self.assertEqual(form.fields['last_name'].max_length, 255)
            self.assertFalse(form.fields['last_name'].required)
            self.assertEqual(form.fields['last_name'].label, '')
            self.assertIsInstance(form.fields['last_name'].widget, forms.TextInput)
            self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Search by Last name')

        def test_task_type_search_form(self):
            form = TaskTypeSearchForm()
            self.assertIsInstance(form.fields['name'], forms.CharField)
            self.assertEqual(form.fields['name'].max_length, 255)
            self.assertFalse(form.fields['name'].required)
            self.assertEqual(form.fields['name'].label, '')
            self.assertIsInstance(form.fields['name'].widget, forms.TextInput)
            self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Search by Type')

        def test_position_search_form(self):
            form = PositionSearchForm()
            self.assertIsInstance(form.fields['name'], forms.CharField)
            self.assertEqual(form.fields['name'].max_length, 255)
            self.assertFalse(form.fields['name'].required)
            self.assertEqual(form.fields['name'].label, '')
            self.assertIsInstance(form.fields['name'].widget, forms.TextInput)
            self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Search by Position')


class TestWorkerForms(unittest.TestCase):
    def test_worker_creation_form(self):
        form = WorkerCreationForm()
        self.assertIsInstance(form, UserCreationForm)
        self.assertEqual(form._meta.model, Worker)
        self.assertEqual(form.Meta.fields, UserCreationForm.Meta.fields + ("first_name", "last_name", "position",))

    def test_worker_update_form(self):
        form = WorkerUpdateForm()
        self.assertEqual(form._meta.model, Worker)
        self.assertEqual(form.Meta.fields, ("username", "first_name", "last_name", "position",))


class TestCustomPasswordChangeForm(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_custom_password_change_form_widgets(self):
        form = CustomPasswordChangeForm(user=self.user)
        self.assertIsInstance(form, PasswordChangeForm)
        self.assertIn('class="form-control"', str(form))
        self.assertIn('placeholder="Старий пароль"', str(form))
        self.assertIn('placeholder="Новий пароль"', str(form))
        self.assertIn('placeholder="Підтвердження нового паролю"', str(form))