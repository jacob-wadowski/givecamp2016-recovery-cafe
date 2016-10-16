# -*- coding: utf-8 -*-


"""recoverycafe_timecard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='homepage'),
    url(r'^login/', include('login.urls')),
    url(r'^accounts/login/$', include('login.urls')),#necessary for @login_required failed
    url(r'^admin/', admin.site.urls),
    url(r'^timecard/', include('timecard.urls')),
    url(r'^adminView/', include('timecard_admin.urls')),

    # REST API
    url(r'^api/', include('recoverycafe_timecard.routers', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls',
            namespace='rest_framework')),
]
