from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.render_volunteer_page, name='render_volunteer_page'),
    url(r'^post/$', views.receive_json, name='receive_json'),
]
