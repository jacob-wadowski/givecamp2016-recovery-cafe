from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse

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

    # queryset_tasks = Task.objects.all()  # List of tasks
    # queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    # queryset_task_list_refreshed = Task.objects.all()
    # # url = reverse(render_admin_page, kwargs={'task_list': queryset_task_list_refreshed})
    # url = reverse(render_admin_page, {'volunteer_list': queryset_volunteers, 'task_list': queryset_tasks, 'reports': queryset_reports})
    # return redirect(url)

    # tbl_html = render_to_string('task_tbl_contents.html', {'task_list': queryset_task_list_refreshed})
    # result = {'html': tbl_html}
    # return HttpResponse(QueryDict(request.body), content_type='application/json')
    # return HttpResponse("<script>console.log('yo.')</script>")

    # Task.objects.create(task_name=task_name_text)
    # queryset_task_list_refreshed = Task.objects.all()
    # return render(request, 'task_tbl_contents.html', {'task_list': queryset_task_list_refreshed})
    #
    #
    # return render(request, 'task_tbl_contents.html', {'new_task_name': task_name_text, 'new_task_record': task_newest_entry})
