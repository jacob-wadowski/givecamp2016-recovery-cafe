from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render

import json

from .models import Task, PunchTime


DB_CURSOR = connection.cursor()


def dict_fetchall(cursor):
    "Return all rows from a cursor as a dict"

    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def receive_json(request):
    data = {"name": "Jacob Wadowski", "event": "Check In"}
    return HttpResponse(json.dumps(data), content_type='application/json')


def render_volunteer_page(request):
    return render(request, 'volunteer.html')


def render_admin_volunteers_page(request):
    queryset_volunteers = DB_CURSOR.execute('SELECT * FROM view_last_known_status')
    return render(request, 'admin_volunteers.html', {'volunteer_list': dict_fetchall(queryset_volunteers)})


def render_admin_tasks_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks
    return render(request, 'admin_tasks.html', {'task_list': queryset_tasks})


def render_admin_reports_page(request):
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'admin_reports.html', {'reports': queryset_reports})
