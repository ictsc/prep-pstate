from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from pstate.views import index
from pstate.views.admin.registers import ParticipantRegisterView, TeamRegisterView

urlpatterns = [
    path('', index, name='index'),
    path('pstate/', index, name='index'),
    # Django admin
    path('pstate/admin/', admin.site.urls),
    # 管理者ページ
    path('pstate/manage/', include('pstate.urls.admin')),
    # 参加者向けページ
    path('pstate/user/', include('pstate.urls.user')),
    # auth
    url(r'^pstate/auth/login/$', auth_views.login, {'template_name': 'admin_pages/auth/login.html'}, name='login'),
    url(r'^pstate/auth/logout/$', auth_views.logout, {'next_page': '/pstate/auth/login'}, name='logout'),
    # url(r'^password/$', views.change_password, name='change_password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 登録フォームの制御.
if settings.IS_TEAM_REGISTER_FORM_ENABLED:
    urlpatterns.append(url('pstate/register/team/$', TeamRegisterView.as_view(), name='team-register'))
if settings.IS_USER_REGISTER_FORM_ENABLED:
    urlpatterns.append(url('pstate/register/participant/$', ParticipantRegisterView.as_view(), name='participant-register'))
