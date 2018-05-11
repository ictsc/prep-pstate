from django.conf.urls import url
from django.urls import path

from pstate.views.user import index, dashboard, ProblemListView, ProblemDetailView, ProblemEnvironmentListView, \
    ProblemEnvironmentDetailView, TeamDetailView, TeamUpdateView, change_password

app_name = 'pstate-user'
urlpatterns = [
    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),
    # problems
    url(r'^problems/$', ProblemListView.as_view(), name='problem-list'),
    url(r'^problems/(?P<pk>[0-9]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    # problem_environments
    url(r'^problem_environments/$', ProblemEnvironmentListView.as_view(), name='problemenvironment-list'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/$', ProblemEnvironmentDetailView.as_view(), name='problemenvironment-detail'),
    # team
    url(r'^team/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^team/edit$', TeamUpdateView.as_view(), name='team-edit'),
    url(r'^team/change_password/$', change_password, name='change_password'),
]
