from django.conf.urls import url
from django.urls import path

from pstate import views

from pstate.views import ParticipantListView, ParticipantCreateView, TeamListView, TeamCreateView, TeamDetailView, TeamUpdateView, TeamDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    url(r'^participants/$', ParticipantListView.as_view(), name='participant-list'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='participant-add'),
    url(r'^teams/$', TeamListView.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^teams/add/$', TeamCreateView.as_view(), name='team-add'),
    url(r'^teams/(?P<pk>[0-9]+)/edit/$', TeamUpdateView.as_view(), name='team-edit'),
    url(r'^teams/(?P<pk>[0-9]+)/delete/$', TeamDeleteView.as_view(), name='team-delete'),
]
