from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.render_admin_page, name='render_admin_page'),
]