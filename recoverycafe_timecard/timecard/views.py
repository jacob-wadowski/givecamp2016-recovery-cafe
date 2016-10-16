from django.shortcuts import render
from django.http import HttpResponse

import json

# Create your views here.

from .forms import PostForm
from .models import Task, PunchTime

DB_CURSOR = connection.cursor()


def dict_fetchall(cursor):
    "Return all rows from a cursor as a dict"

    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def render_volunteer_page(request):
    return render(request, 'volunteer.html')

def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')
