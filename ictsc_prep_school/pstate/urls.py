from django.conf.urls import url
from django.urls import path

from pstate import views

from pstate.views import ParticipantListView, ParticipantCreateView,\
    TeamListView, TeamCreateView, TeamDetailView, TeamUpdateView, TeamDeleteView,\
    ParticipantUpdateView, ParticipantDeleteView,\
    ProblemListView, ProblemDetailView, ProblemCreateView,\
    ProblemEnvironmentListView, ProblemEnvironmentDetailView, ProblemEnvironmentCreateView, ProblemEnvironmentUpdateView, ProblemEnvironmentDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    # auth
    path('login/', views.login, name='login'),
    # teams
    url(r'^teams/$', TeamListView.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^teams/add/$', TeamCreateView.as_view(), name='team-add'),
    url(r'^teams/(?P<pk>[0-9]+)/edit/$', TeamUpdateView.as_view(), name='team-edit'),
    url(r'^teams/(?P<pk>[0-9]+)/delete/$', TeamDeleteView.as_view(), name='team-delete'),
    # participants
    url(r'^participants/$', ParticipantListView.as_view(), name='participant-list'),
    url(r'^participants/(?P<pk>[0-9]+)/$', views.ParticipantDetailView.as_view(), name='participant-detail'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='participant-add'),
    url(r'^participants/(?P<pk>[0-9]+)/edit/$', views.ParticipantUpdateView.as_view(), name='participant-edit'),
    url(r'^participants/(?P<pk>[0-9]+)/delete/$', views.ParticipantDeleteView.as_view(), name='participant-delete'),
    # problems
    url(r'^problems/$', ProblemListView.as_view(), name='problem-list'),
    url(r'^problems/(?P<pk>[0-9]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^problems/add/$', ProblemCreateView.as_view(), name='problem-create'),
    # problem_environments
    url(r'^problem_environments/$', ProblemEnvironmentListView.as_view(), name='problemenvironment-list'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/$', ProblemEnvironmentDetailView.as_view(), name='problemenvironment-detail'),
    url(r'^problem_environments/add/$', ProblemEnvironmentCreateView.as_view(), name='problemenvironment-create'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/edit/$', ProblemEnvironmentUpdateView.as_view(), name='problemenvironment-edit'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/delete/$', ProblemEnvironmentDeleteView.as_view(), name='problemenvironment-delete'),
]
