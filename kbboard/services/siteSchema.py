from rest_framework.schemas.coreapi import AutoSchema


class SiteSchema(AutoSchema):
    """Custom schema."""

    def get_link(self, path, method, base_url):
        """Hide invalid path and method combinations from documentation."""

        if method == 'PATCH' and path == '/tasks/':
            return None
        elif method == 'GET' and path == '/tasks/{id}/':
            return None
        elif method == 'POST' and path == '/tasks/{id}/':
            return None
        return super().get_link(path, method, base_url)
