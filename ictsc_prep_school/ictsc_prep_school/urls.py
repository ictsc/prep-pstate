from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, include
from django.contrib.auth import views as auth_views

from pstate.views import TeamRegisterView, ParticipantRegisterView


def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'admin_pages/index.html')
        else:
            return render(request, 'user_pages/index.html')
    return HttpResponseRedirect('/auth/login/')


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('manage/', include('pstate.urls')),
    path('user/', include('pstate.user_page_urls')),
    url('register/team/$', TeamRegisterView.as_view(), name='team-register'),
    url('register/participant/$', ParticipantRegisterView.as_view(), name='participant-register'),
    # auth
    url(r'^auth/login/$', auth_views.login, {'template_name': 'admin_pages/auth/login.html'}, name='login'),
    url(r'^auth/logout/$', auth_views.logout, {'next_page': '/auth/login'}, name='logout'),
    # url(r'^password/$', views.change_password, name='change_password'),
]
