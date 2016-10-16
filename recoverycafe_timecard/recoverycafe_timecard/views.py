from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from timecard.views import render_volunteer_page
from timecard_admin.views import render_admin_page
from login.views import login


class HomePage(generic.View):
    """
    Show the approprioate view based on user permssions/authentication
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse(login)) 
        if (user.has_perm('login.supervision_permission')):
            return HttpResponseRedirect(reverse(render_admin_page))
        else:
            return HttpResponseRedirect(reverse(render_volunteer_page))

