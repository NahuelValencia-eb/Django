from django.test import TestCase
from parameterized import parameterized
from django.contrib.auth.models import User
from todolist_app.models import Task, Priority
from datetime import datetime


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Nahuel', password='coso')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

    def test_same_id_priority(self):
        priority = Priority.objects.create(name="Normal")
        self.assertEqual(4, priority.id)

    # @parameterized.expand([
    #     ('Low', 'Low'),
    #     ('Normal', 'Normal'),
    #     ('Urgent', 'Urgent'),
    # ])
    def test_same_name_priority(self):
        priority = Priority.objects.create(name="Low")
        self.assertEqual(priority.name, "Low")

    def test_valid_name_priority(self):
        priority = Priority.objects.create(name="High")
        self.assertNotEqual("Urgent", priority.name)

    def test_task_creation(self):
        priority = Priority.objects.create(name="Low")
        task = Task.objects.create(name="Tarea1", created=datetime.now(), changed=datetime.now(), priority=priority, author=self.user, done=False, id_event=13243546)
        self.assertEqual(task.name, "Tarea1")
