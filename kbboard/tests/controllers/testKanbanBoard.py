from datetime import datetime
from datetime import timedelta
from unittest import skip

from django.test import LiveServerTestCase
import json
from kbboard.controllers import KanbanBoard
from kbboard.models import Task
import pytz

# python manage.py test kbboard.tests.controllers.testKanbanBoard


class TestKanbanBoard(LiveServerTestCase):
    """Tests for KanbanBoard"""

    def setUp(self):
        Task.objects.bulk_create([
            Task(title='test-task-1'),
            Task(title='test-task-2')
        ])

    def test_get_site_root(self):
        """Test: Method GET, URI /
        Request site root."""

        response = self.client.get('/')
        self.assertTrue(404, response.status_code)

    def test_get_tasks(self):
        """Test: Method GET, URI /tasks/
        Get all tasks."""

        response = self.client.get('/tasks/')
        self.assertTrue(200, response.status_code)

        decoded = response.content.decode('utf8')
        tasks = json.loads(decoded)
        self.assertEqual(2, len(tasks))

    def test_create_task(self):
        """Test: Method POST, URI /tasks/
        Create task."""

        data = {
            'title': 'test-task-3'
        }
        response = self.client.post('/tasks/', data)
        self.assertTrue(201, response.status_code)

        expected = {
            'id': 3,
            'title': 'test-task-3',
            'start_time': None,
            'end_time': None,
            'status': 0,
            'payment': 0
        }
        actual = json.loads(response.content.decode('utf8'))
        self.assertEqual(expected, actual)

    def test_start_task(self):
        """Test: Method PATCH, URI /tasks/<int:id>/
        Update task. Set status = IN_PROGRESS."""

        data = {
            'status': Task.Statuses.IN_PROGRESS
        }
        first = Task.objects.first()
        uri = f'/tasks/{first.id}/'
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(205, response.status_code)

        actual = json.loads(response.content.decode('utf8'))
        self.assertEqual(Task.Statuses.IN_PROGRESS, actual['status'])

        expected = datetime.now()
        dt_str = actual['start_time']
        # Creates date object from string like '2020-09-15T20:08:14.312Z'.
        actual = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(expected.date(), actual.date())

    def test_finish_task(self):
        """Test: Method PATCH, URI /tasks/<int:id>/
        Update task. Set status = DONE."""

        first = Task.objects.first()
        first.status = Task.Statuses.IN_PROGRESS
        start_dt = datetime.now(tz=pytz.UTC)
        start_dt = start_dt - timedelta(days=1)
        start_dt = start_dt.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        first.start_time = start_dt
        first.save()

        data = {
            'status': Task.Statuses.DONE
        }
        first = Task.objects.get(id=first.id)
        uri = f'/tasks/{first.id}/'
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(205, response.status_code)

        task = json.loads(response.content.decode('utf8'))
        self.assertEqual(Task.Statuses.DONE, task['status'])

        dt_str = task['end_time']
        # Creates date object from string like '2020-09-15T20:08:14.312Z'.
        end_dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_dt = pytz.utc.localize(end_dt)
        self.assertTrue(start_dt < end_dt)

        self.assertRegex(str(task['payment']), '\d+\.\d{2}')

    def test_same_status(self):
        """Test: Method PATCH, URI /tasks/<int:id>/
        Update task. Set status = TODO."""

        data = {
            'status': Task.Statuses.TODO
        }
        first = Task.objects.first()
        uri = f'/tasks/{first.id}/'
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(304, response.status_code)

    def test_previous_status(self):
        """Test: Method PATCH, URI /tasks/<int:id>/
        Update task. Set status = 1. And then 0."""

        data = {
            'status': Task.Statuses.IN_PROGRESS
        }
        first = Task.objects.first()
        uri = f'/tasks/{first.id}/'
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(205, response.status_code)

        data = {
            'status': Task.Statuses.TODO
        }
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(409, response.status_code)

    def test_incorrect_status(self):
        """Test: Method PATCH, URI /tasks/<int:id>/
        Update task. Set status = 999."""

        data = {
            'status': 999
        }
        first = Task.objects.first()
        uri = f'/tasks/{first.id}/'
        response = self.client.patch(uri, data, content_type='application/json')
        self.assertTrue(400, response.status_code)

    def test_payment_formula(self):
        """Test payment formula."""

        start_dt = datetime.now(tz=pytz.UTC)
        start_dt = start_dt - timedelta(days=1)
        start_dt = start_dt.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        end_dt = datetime.now(tz=pytz.UTC)
        end_dt = start_dt - timedelta(days=1)
        end_dt = start_dt.replace(
            hour=14, minute=15, second=45, microsecond=0
        )
        delta = end_dt - start_dt
        hours = delta.total_seconds() / 3600
        payment = hours * KanbanBoard.COST_PER_HOUR
        self.assertEqual(262.5, payment)
