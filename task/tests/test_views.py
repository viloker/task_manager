from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task.models import Task, TaskType, Position

INDEX_URL = reverse("task:index")
TASK_LIST_URL = reverse("task:task-list")
WORKER_LIST_URL = reverse("task:worker-list")


class PublicTaskTest(TestCase):

    def test_login_required(self):
        urls = [INDEX_URL, TASK_LIST_URL, WORKER_LIST_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)


class PrivateTaskTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="QA")

    def test_index_page_context(self):
        Task.objects.create(
            name="Urgent Task", deadline="2026-12-12",
            priority="Urgent", task_type=self.task_type
        )
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_urgent_tasks"], 1)

    def test_retrieve_task_list(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task/task_list.html")

    def test_task_search_filter(self):
        Task.objects.create(name="Fix bug", deadline="2026-12-12", task_type=self.task_type)
        Task.objects.create(name="Write docs", deadline="2026-12-12", task_type=self.task_type)

        response = self.client.get(TASK_LIST_URL, {"name": "Fix"})
        self.assertContains(response, "Fix bug")
        self.assertNotContains(response, "Write docs")

    def test_my_task_list_queryset(self):
        my_task = Task.objects.create(name="My", deadline="2026-12-12", task_type=self.task_type)
        other_task = Task.objects.create(name="Other", deadline="2026-12-12", task_type=self.task_type)

        my_task.assignees.add(self.user)

        response = self.client.get(reverse("task:my-task"))
        self.assertContains(response, "My")
        self.assertNotContains(response, "Other")

    def test_task_detail_post_mark_completed(self):
        task = Task.objects.create(
            name="Not Done", deadline="2026-12-12",
            is_completed=False, task_type=self.task_type
        )
        url = reverse("task:task-detail", kwargs={"pk": task.id})

        response = self.client.post(url)
        task.refresh_from_db()

        self.assertTrue(task.is_completed)
        self.assertEqual(response.status_code, 200)


class WorkerViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="password"
        )
        self.client.force_login(self.user)
        self.position = Position.objects.create(name="Developer")

    def test_worker_list_search(self):
        get_user_model().objects.create_user(username="ivan", password="p", position=self.position)
        get_user_model().objects.create_user(username="petro", password="p", position=self.position)

        response = self.client.get(WORKER_LIST_URL, {"username": "ivan"})
        self.assertContains(response, "ivan")
        self.assertNotContains(response, "petro")

    def test_worker_delete_redirect(self):
        worker_to_delete = get_user_model().objects.create_user(
            username="to_delete", password="p"
        )
        url = reverse("task:worker-delete", kwargs={"pk": worker_to_delete.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse("task:task-list"))
        self.assertFalse(get_user_model().objects.filter(id=worker_to_delete.id).exists())
