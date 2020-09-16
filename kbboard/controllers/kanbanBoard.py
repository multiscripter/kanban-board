from datetime import datetime
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import json

from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from kbboard.models import Task
import pytz


class KanbanBoard(View):

    COST_PER_HOUR = 1000

    #@method_decorator(csrf_protect, 'dispatch')
    #@method_decorator(ensure_csrf_cookie, 'dispatch')
    def get(self, request, *args, **kwargs):
        """Handles GET requests."""

        tasks = Task.objects.all()
        objs = []
        if tasks:
            for task in tasks:
                obj = self.map_to_json(task)
                objs.append(obj)
        return JsonResponse(objs, safe=False)

    #@method_decorator(csrf_protect, 'dispatch')
    #@method_decorator(ensure_csrf_cookie, 'dispatch')
    def post(self, request, *args, **kwargs):
        """Handles POST requests."""

        task = Task()
        task.title = request.POST['title']
        task.save()
        obj = self.map_to_json(task)
        return JsonResponse(obj, safe=False, status=201)

    def patch(self, request, id, *args, **kwargs):
        """Handles PATCH requests."""

        obj = {}
        task = Task.objects.get(id=int(id))
        body = json.loads(request.body)
        body['status'] = int(body['status'])
        update = [task.Statuses.IN_PROGRESS, task.Statuses.DONE]
        if body['status'] in update:
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
        return JsonResponse(obj, safe=False, status=205)

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
