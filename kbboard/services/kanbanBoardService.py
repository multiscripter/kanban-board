from datetime import datetime
import json
from kbboard.models import Task
import pytz


class KanbanBoardService:

    COST_PER_HOUR = 1000

    def create_task(self, request):
        params = {
            'data': None,
            'status': 201 # Created.
        }
        task = Task()
        task.title = request.data['title']
        task.save()
        params['data'] = self.map_to_json(task)
        return params

    def get_tasks(self):
        tasks = Task.objects.all()
        objects = []
        if tasks:
            for task in tasks:
                obj = self.map_to_json(task)
                objects.append(obj)
        return {'data': objects}

    def update_task(self, request, id):
        params = {
            'data': None,
            'status': 205  # Reset Content.
        }
        task = Task.objects.get(id=int(id))
        body = json.loads(request.body)
        update = [
            task.Statuses.TODO, task.Statuses.IN_PROGRESS, task.Statuses.DONE
        ]
        if body['status'] in update:
            if body['status'] - 1 == task.status:
                task.status = body['status']
                if body['status'] == task.Statuses.IN_PROGRESS:
                    task.start_time = datetime.now(tz=pytz.UTC)
                elif task.status == task.Statuses.DONE:
                    task.end_time = datetime.now(tz=pytz.UTC)
                    delta = task.end_time - task.start_time
                    hours = delta.total_seconds() / 3600
                    task.payment = hours * KanbanBoardService.COST_PER_HOUR
                    task.payment = round(task.payment, 2)
                task.save()
                params['data'] = self.map_to_json(task)
            elif body['status'] == task.status:
                params['status'] = 304  # Not Modified.
            else:
                params['status'] = 409  # Conflict.
        else:
            params['status'] = 400  # Bad Request.
        return params

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
