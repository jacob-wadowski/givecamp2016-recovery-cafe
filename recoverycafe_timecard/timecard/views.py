from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

import json
from .models import LastKnownStatus, PunchTime, Task


def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def render_volunteer_page(request):
    print request
    queryset_tasks = Task.objects.all()  # List of tasks
    #TODO: Need to find out why request.session['branch'] is resulting in key error
    #return render(request, 'volunteer.html', {'task_list': queryset_tasks, 'branch': request.session['branch']})
    return render(request, 'volunteer.html', {'task_list': queryset_tasks, 'branch': 'seattle'})
