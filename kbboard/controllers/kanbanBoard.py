from datetime import datetime
import json
from kbboard.models import Task
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response


class KanbanBoard(APIView):

    COST_PER_HOUR = 1000

    def get(self, request, *args, **kwargs):
        """Handles GET requests."""

        tasks = Task.objects.all()
        objects = []
        if tasks:
            for task in tasks:
                obj = self.map_to_json(task)
                objects.append(obj)
        return Response(objects)

    def post(self, request, *args, **kwargs):
        """Handles POST requests."""

        task = Task()
        task.title = request.data['title']
        task.save()
        obj = self.map_to_json(task)
        return Response(obj, status=201)

    def patch(self, request, id, *args, **kwargs):
        """Handles PATCH requests."""

        obj = {}
        status = 205 # Reset Content.
        task = Task.objects.get(id=int(id))
        body = json.loads(request.body)
        body['status'] = int(body['status'])
        update = [
            task.Statuses.TODO, task.Statuses.IN_PROGRESS, task.Statuses.DONE
        ]
        if body['status'] in update:
            if body['status'] > task.status:
                task.status = body['status']
                if task.status == task.Statuses.IN_PROGRESS:
                    task.start_time = datetime.now(tz=pytz.UTC)
                elif task.status == task.Statuses.DONE:
                    task.end_time = datetime.now(tz=pytz.UTC)
                    delta = task.end_time - task.start_time
                    hours = delta.total_seconds() / 3600
                    task.payment = hours * KanbanBoard.COST_PER_HOUR
                    task.payment = round(task.payment, 2)
                task.save()
                obj = self.map_to_json(task)
            elif body['status'] == task.status:
                status = 304 # Not Modified.
            else:
                status = 409 # Conflict.
        else:
            status = 400 # Bad Request.
        return Response(obj, status=status)

    def map_to_json(self,task):
        obj = {
            "id": task.id,
            "title": task.title,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "status": task.status,
            "payment": task.payment
        }
        return obj
