from django.shortcuts import render
from django.http import HttpResponse

import json

# Create your views here.

from .forms import PostForm

def render_volunteer_page(request):
    return render(request, 'volunteer.html')

def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')
