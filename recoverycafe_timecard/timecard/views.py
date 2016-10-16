from django.shortcuts import render

# Create your views here.

from .forms import PostForm
from .models import Volunteer

def render_volunteer_page(request):
    return render(request, 'volunteer.html')

def render_admin_volunteers_page(request):
    queryset_volunteers = Volunteer.objects.all()
    return render(request, 'admin_volunteers.html', {'volunteer_list': queryset_volunteers})
