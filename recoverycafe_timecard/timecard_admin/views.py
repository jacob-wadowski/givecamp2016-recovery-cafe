from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.db import connection, transaction
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from timecard.models import LastKnownStatus, PunchTime, Task, Volunteer
from .utils.import_volunteers import get_volunteer_records
from .utils.export_data import get_report_data
from .utils.excel_report_creator import excel_report_creator

from login.models import *

from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages

import json, re

DB_CURSOR = connection.cursor()

@login_required
@user_passes_test(lambda u: u.has_perm(FULL_SUPERVISION_PERMISSION))
def render_admin_page(request):
    queryset_volunteers = LastKnownStatus.objects.filter(punch_type_latest='IN')
    queryset_tasks = Task.objects.all()  # List of tasks
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    queryset_volunteer_master_list = Volunteer.objects.all()    #List of all volunteers in the database
    return render(request, 'admin.htm', {'volunteer_list': queryset_volunteers, 'task_list': queryset_tasks, 'reports': queryset_reports, 'volunteers_master_list': queryset_volunteer_master_list})

@login_required
@user_passes_test(lambda u: u.has_perm(FULL_SUPERVISION_PERMISSION))
def render_admin_volunteers_page(request):
    queryset_volunteers = LastKnownStatus.objects.all()
    return render(request, 'admin_volunteers.html', {'volunteer_list': queryset_volunteers})

@login_required
@user_passes_test(lambda u: u.has_perm(FULL_SUPERVISION_PERMISSION))
def render_admin_tasks_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks
    return render(request, 'admin_tasks.html', {'task_list': queryset_tasks})

@login_required
@user_passes_test(lambda u: u.has_perm(FULL_SUPERVISION_PERMISSION))
def render_admin_reports_page(request):
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'admin_reports.html', {'reports': queryset_reports})

@login_required
@user_passes_test(lambda u: u.has_perm(FULL_SUPERVISION_PERMISSION))
def render_volunteer_master_list_page(request):
    queryset_ = Task.objects.all()  # List of tasks
    queryset_volunteer_master_list = Volunteer.objects.all()    #List of all volunteers in the database
    return render(request, 'volunteers-master.html', {'volunteers_master_list': queryset_volunteer_master_list})


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
            
        messages.add_message(request, messages.INFO, 'Imported %d volunteers' % len(records))
        newUsers = True

    return HttpResponseRedirect(reverse(render_admin_page))


class ReportView(generic.View):
    """
    Generate XLXS file downloads based off of POST parameters.
    """
    def post(self, request, *args, **kwargs):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        return self.generate_response(start_date, end_date)

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        return self.generate_response(start_date, end_date)

    def format_date(self, date_text):
        datepicker_format = re.compile('\d+/\d+/\d+')
        if datepicker_format.match(date_text):
            date_array = date_text.split('/')
            MM = date_array[0]
            DD = date_array[1]
            YYYY = date_array[2]
            return YYYY + '-' + MM + '-' + DD
        else:
            return date_text

    def generate_response(self, start_date, end_date):
        data = get_report_data(
                self.format_date(start_date),
                self.format_date(end_date))
        # Generate XLSX file from data
        xlsx = excel_report_creator(data)
        # ... Magic is done. Return response.
        attachment = 'attachment; filename="Report Data.xlsx"'
        response = HttpResponse(xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = attachment
        return response
        

