from django.http import HttpResponse, QueryDict
from django.shortcuts import render

import json

from timecard.models import LastKnownStatus, PunchTime, Task


def render_admin_page(request):
    queryset_volunteers = LastKnownStatus.objects.filter(punch_type_latest='IN')
    queryset_tasks = Task.objects.all()  # List of tasks
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'admin.htm', {'volunteer_list': queryset_volunteers, 'task_list': queryset_tasks, 'reports': queryset_reports})


def render_admin_volunteers_page(request):
    queryset_volunteers = LastKnownStatus.objects.all()
    return render(request, 'admin_volunteers.html', {'volunteer_list': queryset_volunteers})


def render_admin_tasks_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks
    return render(request, 'admin_tasks.html', {'task_list': queryset_tasks})


def render_admin_reports_page(request):
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'admin_reports.html', {'reports': queryset_reports})


def add_task(request):
    task_name_text = QueryDict(request.body)['provided_task_name']
    new_task = Task.objects.create(task_name=task_name_text)
    task_newest_entry = Task.objects.filter(id=new_task.id)[0]  # Type: <class 'timecard.models.Task'>
    return HttpResponse(json.dumps({'task_id': task_newest_entry.id, \
                                    'task_name': task_newest_entry.task_name}), content_type='application/json')


def remove_task(request):
    selected_task_id = QueryDict(request.body)['button_task_id']
    Task.objects.filter(id=selected_task_id).delete()
    return HttpResponse(json.dumps({'task_id': selected_task_id}), content_type='application/json')
