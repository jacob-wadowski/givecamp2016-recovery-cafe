from django.shortcuts import render

# Create your views here.

from .forms import PostForm
from .models import Volunteer, Task, PunchTime
# TODO: Pull in constant with context on currently-selected branch

def render_volunteer_page(request):
    return render(request, 'volunteer.html')

def render_admin_volunteers_page(request):
    queryset_volunteers = Volunteer.objects.all()
    return render(request, 'volunteers.html', {'volunteer_list': queryset_volunteers})

def render_admin_tasks_page(request):
    queryset_tasks = Task.objects.all()  # List of tasks  # TODO: Filter on branch
    return render(request, 'tasks.html', {'task_list': queryset_tasks})

def render_admin_reports_page(request):
    queryset_reports = PunchTime.objects.all()  # One workbook w/multiple sheets
    return render(request, 'reports.html', {'reports': queryset_reports})
