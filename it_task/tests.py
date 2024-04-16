from django.test import TestCase
from django.contrib.auth import get_user_model
from it_task.models import TaskType, Position, Task

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
