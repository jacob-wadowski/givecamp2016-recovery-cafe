from django.http import HttpResponse
from django.shortcuts import render

import json


def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def render_volunteer_page(request):
    return render(request, 'volunteer.html', {'branch': request.session['branch']})
