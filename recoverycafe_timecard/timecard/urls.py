from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.render_volunteer_page, name='render_volunteer_page'),
    url(r'^admin/volunteers/', views.render_admin_volunteers_page, name='render_admin_volunteers_page'),
    url(r'^admin/tasks/', views.render_admin_tasks_page, name='render_admin_tasks_page'),
    url(r'^admin/reports/', views.render_admin_reports_page, name='render_admin_reports_page'),
]
