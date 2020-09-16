from datetime import datetime
import json
from kbboard.models import Task
import pytz
import re


class KanbanBoardService:
    COST_PER_HOUR = 1000

    def create_task(self, request):
        is_valid = True
        params = {
            'data': {},
            'status': 201  # Created.
        }
        if request.path != '/tasks/':
            params['data'] = {'error': 'incorrect path'}
            params['status'] = 404  # Not Found.
            is_valid = False
        if is_valid and 'title' not in request.data:
            params['data'] = {'error': 'title is not set'}
            params['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid and not request.data['title'].strip():
            params['data'] = {'error': 'title is empty'}
            params['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            task = Task()
            task.title = request.data['title'].strip()
            task.save()
            params['data'] = self.map_to_json(task)
        return params

    def get_tasks(self, request):
        is_valid = True
        params = {
            'data': {},
            'status': 200  # OK.
        }
        if request.path != '/tasks/':
            params['data'] = {'error': 'incorrect path'}
            params['status'] = 404  # Not Found.
            is_valid = False
        if is_valid:
            tasks = Task.objects.all()
            objects = []
            if tasks:
                for task in tasks:
                    obj = self.map_to_json(task)
                    objects.append(obj)
            params['data'] = objects
        return params

    def update_task(self, request, id):
        is_valid = True
        params = {
            'data': {},
            'status': 205  # Reset Content.
        }
        body = dict()
        if not re.match(r'/tasks/\d+/', request.path):
            params['data'] = {'error': 'incorrect path'}
            params['status'] = 404  # Not Found.
            is_valid = False
        if is_valid and not request.body:
            params['data'] = {'error': 'no body'}
            params['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            body = json.loads(request.body)
            if 'status' not in body:
                params['data'] = {'error': 'status is not set'}
                params['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid and '' == body['status']:
            params['data'] = {'error': 'status is empty'}
            params['status'] = 400  # Bad Request.
            is_valid = False
        if is_valid:
            update = [
                Task.Statuses.TODO,
                Task.Statuses.IN_PROGRESS,
                Task.Statuses.DONE
            ]
            if body['status'] not in update:
                params['data'] = {'error': 'unknown status'}
                params['status'] = 400  # Bad Request.
                is_valid = False
        if is_valid:
            task = Task.objects.get(id=int(id))
            if body['status'] == task.status:
                params['data'] = {'error': 'status is not changed'}
                params['status'] = 400  # Bad Request.
                is_valid = False
            elif body['status'] - 1 != task.status:
                params['data'] = {'error': 'incorrect status'}
                params['status'] = 409  # Conflict.
                is_valid = False
        if is_valid:
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
        return params

    def map_to_json(self, task):
        obj = {
            "id": task.id,
            "title": task.title,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "status": task.status,
            "payment": task.payment
        }
        return obj
