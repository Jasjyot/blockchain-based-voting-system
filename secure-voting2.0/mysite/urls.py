from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from mysite.core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^poll/$', core_views.poll, name='poll'),
    url(r'^$', core_views.poll, name='poll'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^verify/$', core_views.verify, name='verify')
]
