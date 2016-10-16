from django.http import HttpResponse
from django.shortcuts import render

import json
from .models import LastKnownStatus, PunchTime, Task


def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def render_volunteer_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks
    return render(request, 'volunteer.html', {'task_list': queryset_tasks})
