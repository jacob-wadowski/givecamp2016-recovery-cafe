from django.shortcuts import render

# Create your views here.


def render_admin_page(request):
	return render(request, 'adminView/admin.htm')