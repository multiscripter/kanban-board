from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    TITLE = 'Kanban board REST service API'
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title=SwaggerSchemaView.TITLE,
            url='http://kanban-board.bot.net/'
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
