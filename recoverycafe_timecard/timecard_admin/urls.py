from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.render_admin_page, name='render_admin_page'),
    url(r'^admin/volunteers/', views.render_admin_volunteers_page, name='render_admin_volunteers_page'),
    url(r'^admin/tasks/', views.render_admin_tasks_page, name='render_admin_tasks_page'),
    url(r'^admin/reports/', views.render_admin_reports_page, name='render_admin_reports_page'),
    url(r'^admin/add_task/', views.add_task, name='add_task'),
    url(r'^admin/remove_task/', views.remove_task, name='remove_task'),
]
