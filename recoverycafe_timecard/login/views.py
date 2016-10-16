from django.http import *
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authLogin

from timecard.views import render_volunteer_page
from timecard_admin.views import render_admin_page
from timecard.models import Branch


def login(request):
    logout(request)
    username = password = branch = ''
    queryset_branches = Branch.objects.all()

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        branch = request.POST.get('branch', Branch.objects.first())

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session['branch']=branch
            authLogin(request, user)

        try:
            if (user.has_perm('login.supervision_permission')):
                return HttpResponseRedirect(reverse(render_admin_page))
            else:
                return HttpResponseRedirect(reverse(render_volunteer_page))

        except AttributeError:  # If user account doesn't exist/some other error, show friendly error message
            response = HttpResponseBadRequest("Invalid or missing login info. Make sure no fields are empty, and that the username exists in the system.")
            return render(request, 'login/login.html', {'response': response.content})

    return render(request, 'login/login.html', {'branches': queryset_branches})
