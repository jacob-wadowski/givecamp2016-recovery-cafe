from django.shortcuts import render

# Create your views here.

from .forms import PostForm

def render_volunteer_page(request):
    form = PostForm()
    return render(request, 'volunteer.html', {'form': form})
