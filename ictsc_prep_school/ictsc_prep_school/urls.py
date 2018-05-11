from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from pstate.views import index
from pstate.views.admin.registers import ParticipantRegisterView, TeamRegisterView

urlpatterns = [
    path('', index, name='index'),
    # Django admin
    path('admin/', admin.site.urls),
    # 管理者ページ
    path('manage/', include('pstate.urls.admin')),
    # 参加者向けページ
    path('user/', include('pstate.urls.user')),
    # 登録フォーム
    url('register/team/$', TeamRegisterView.as_view(), name='team-register'),
    url('register/participant/$', ParticipantRegisterView.as_view(), name='participant-register'),
    # auth
    url(r'^auth/login/$', auth_views.login, {'template_name': 'admin_pages/auth/login.html'}, name='login'),
    url(r'^auth/logout/$', auth_views.logout, {'next_page': '/auth/login'}, name='logout'),
    # url(r'^password/$', views.change_password, name='change_password'),
]
