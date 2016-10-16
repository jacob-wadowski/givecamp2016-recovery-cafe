from django.shortcuts import render

# Create your views here.

def adminContainer(request):
	return render(request, 'adminView/admin.htm')