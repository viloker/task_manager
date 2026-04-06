from django.test import TestCase

from django.contrib.auth import get_user_model

from .models import TaskType, Task, Position


class ModelTests(TestCase):
    def test_TaskType_str(self):
        task_type = TaskType.objects.create(name="new_task_type")
        self.assertEqual(str(task_type), task_type.name)

    def test_Task_str(self):
        task = Task.objects.create(
            name="new_task",
            description="some description",
            deadline="2020-11-04",
            is_completed=True,
            priority="urgent",
            task_type=TaskType.objects.create(name="name")
        )
        self.assertEqual(str(task), task.name)

    def test_create_task_with_task_type(self):
        task_type = TaskType.objects.create(name="some_type")

        task = Task.objects.create(
            name="new_task",
            description="some description",
            deadline="2020-11-04",
            is_completed=True,
            priority="urgent",
            task_type=task_type
        )
        self.assertEqual(task.task_type, task_type)

    def test_create_task_with_workers(self):
        worker_1 = get_user_model().objects.create_user(
            username="username_1",
            password="password_1",
        )
        worker_2 = get_user_model().objects.create_user(
            username="username_2",
            password="password_2",
        )
        task = Task.objects.create(
            name="new_task",
            description="some description",
            deadline="2020-11-04",
            is_completed=True,
            priority="urgent",
            task_type=TaskType.objects.create(name="name")
        )

        task.assignees.add(worker_1, worker_2)

        self.assertEqual(
            list(task.assignees.all()),
            [worker_1, worker_2])

    def test_task_related_name_to_worker(self):
        worker_1 = get_user_model().objects.create_user(
            username="username_1",
            password="password_1",
        )

        task = Task.objects.create(
            name="new_task",
            description="some description",
            deadline="2020-11-04",
            is_completed=True,
            priority="urgent",
            task_type=TaskType.objects.create(name="name")
        )
        task.assignees.add(worker_1)

        self.assertEqual(list(worker_1.tasks.all()), [task])

    def test_Worker_str(self):
        worker = get_user_model().objects.create_user(
            username="username",
            password="somepassword",
            position=Position.objects.create(name="name")
        )
        self.assertEqual(
            str(worker),
            f"{worker.username}: ({worker.position})")

    def test_worker_delete_position(self):
        position = Position.objects.create(name="name")

        worker = get_user_model().objects.create_user(
            username="username",
            password="somepassword",
            position=position
        )

        self.assertEqual(worker.position, position)
        position.delete()
        worker.refresh_from_db()
        self.assertIsNone(worker.position,
                          msg="If position will be deleted then"
                              "worker.position must be None")

    def test_create_worker_with_position(self):
        username = "test"
        password = "SomePassword123"
        position = Position.objects.create(name="position")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )

        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)

    def test_Position_str(self):
        position = Position.objects.create(name="name")

        self.assertEqual(str(position), position.name)
