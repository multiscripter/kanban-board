from django.test import TestCase


class TestKanbanBoard(TestCase):
    """Tests for KanbanBoard"""

    def get_tasks(self):
        """Test GET /"""
        response = self.client.get('/')
        html = response.content.decode('utf8')
        print(html)
