from kbboard.services import KanbanBoardService
from rest_framework.views import APIView
from rest_framework.response import Response


class KanbanBoard(APIView):

    def get(self, request, *args, **kwargs):
        """Handles GET requests."""

        service = KanbanBoardService()
        params = service.get_tasks()
        return Response(params['data'])

    def post(self, request, *args, **kwargs):
        """Handles POST requests."""

        service = KanbanBoardService()
        params = service.create_task(request)
        return Response(params['data'], params['status'])

    def patch(self, request, id, *args, **kwargs):
        """Handles PATCH requests."""

        service = KanbanBoardService()
        params = service.update_task(request, id)
        return Response(params['data'], params['status'])
