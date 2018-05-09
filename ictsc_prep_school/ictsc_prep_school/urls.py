from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from pstate.views import TeamRegisterView, ParticipantRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', include('pstate.urls')),
    path('user/', include('pstate.user_page_urls')),
    url('register/team/$', TeamRegisterView.as_view(), name='team-register'),
    url('register/participant/$', ParticipantRegisterView.as_view(), name='participant-register'),
]
