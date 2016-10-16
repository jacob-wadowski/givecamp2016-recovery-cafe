from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.db import connection, transaction
from django.shortcuts import render
from django.urls import reverse

from timecard.models import LastKnownStatus, PunchTime, Task, Volunteer
from utils.import_volunteers import get_volunteer_records

from login.models import *

from django.contrib.auth.decorators import user_passes_test, login_required

import json

DB_CURSOR = connection.cursor()

@login_required
@user_passes_test(lambda u: u.has_perm(SUPERVISIONPERMISSION))
def render_admin_page(request):
    queryset_volunteers = LastKnownStatus.objects.filter(punch_type_latest='IN')
    queryset_tasks = Task.objects.all()  # List of tasks
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'admin.htm', {'volunteer_list': queryset_volunteers, 'task_list': queryset_tasks, 'reports': queryset_reports})

@login_required
@user_passes_test(lambda u: u.has_perm(SUPERVISIONPERMISSION))
def render_admin_volunteers_page(request):
    queryset_volunteers = LastKnownStatus.objects.all()
    return render(request, 'admin_volunteers.html', {'volunteer_list': queryset_volunteers})

@login_required
@user_passes_test(lambda u: u.has_perm(SUPERVISIONPERMISSION))
def render_admin_tasks_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks
    return render(request, 'admin_tasks.html', {'task_list': queryset_tasks})

@login_required
@user_passes_test(lambda u: u.has_perm(SUPERVISIONPERMISSION))
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

@transaction.atomic()
def import_volunteers(request):
    if 'volunteers' in request.FILES:
        f = request.FILES['volunteers']
        records = get_volunteer_records(f.name, f)
        for r in records:
            obj, _ = Volunteer.objects.update_or_create(
                    staff_id=r['staff_id'], defaults=r)

    return HttpResponseRedirect(reverse(render_admin_page))
