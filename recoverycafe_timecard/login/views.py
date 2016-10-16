from django.http import *
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authLogin

def login(request):
    logout(request)
    username = password = branch = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
	branch = request.POST['branch']
	
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
		request.session['branch']=branch
                authLogin(request, user)

		if(user.has_perm('login.supervisor_permission')):
			return HttpResponse("Supervisor level")
		else:
			return HttpResponse("Volunteer level")
    return render(request, 'login/login.html')
