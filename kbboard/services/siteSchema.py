from rest_framework.schemas.coreapi import AutoSchema


# Ошибка: 'staticfiles' is not a registered tag library.
# Must be one of: admin_list admin_modify admin_urls cache i18n
# l10n log rest_framework static tz
# Исправление:
# Открыть index.html (AppData\Local\programs\python\python38\lib\
# site-packages\rest-framework-swagger\index.html)
# Изменить вторую строку с {% load staticfiles %}
# на {% load static %}

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
