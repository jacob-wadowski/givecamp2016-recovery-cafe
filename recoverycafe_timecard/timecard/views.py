from django.shortcuts import render

# Create your views here.

from .forms import PostForm

def render_volunteer_page(request):
    return render(request, 'volunteer.html')
