from django.test import LiveServerTestCase
import json
from kbboard.controllers import SwaggerSchemaView


class TestSwaggerSchemaView(LiveServerTestCase):
    """Test SwaggerSchemaView controller."""

    def test_get(self):
        """Test: Method GET, URI /openapi/
        Get all tasks."""

        response = self.client.get('/openapi/')
        self.assertTrue(200, response.status_code)

        decoded = response.content.decode('utf8')
        actual = json.loads(decoded)
        self.assertEqual(
            SwaggerSchemaView.TITLE, actual['info']['title']
        )
