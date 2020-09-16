from kbboard.services import KanbanBoardService
from kbboard.services.siteSchema import SiteSchema
from rest_framework.views import APIView
from rest_framework.response import Response


class KanbanBoard(APIView):

    schema = SiteSchema()

    def get(self, request, *args, **kwargs):
        """Get tasks."""

        service = KanbanBoardService()
        params = service.get_tasks(request)
        return Response(params['data'], params['status'])

    def post(self, request, *args, **kwargs):
        """Create task."""

        service = KanbanBoardService()
        params = service.create_task(request)
        return Response(params['data'], params['status'])

    def patch(self, request, id, *args, **kwargs):
        """Update task."""

        service = KanbanBoardService()
        params = service.update_task(request, id)
        return Response(params['data'], params['status'])
