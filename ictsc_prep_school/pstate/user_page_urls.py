from django.conf.urls import url
from django.urls import path

from pstate.views import user

from pstate.views.user import ProblemEnvironmentCreateExecuteView, ProblemEnvironmentListView, \
    ProblemEnvironmentDetailView, ProblemListView, ProblemDetailView

app_name = 'pstate-user'
urlpatterns = [
    path('', user.index, name='index'),
    path('dashboard', user.dashboard, name='dashboard'),
    # problems
    url(r'^problems/$', ProblemListView.as_view(), name='problem-list'),
    url(r'^problems/(?P<pk>[0-9]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^problems/(?P<pk>[0-9]+)/problem_environment/add/$', ProblemEnvironmentCreateExecuteView.as_view(), name='problems-problemenvironment-create'),
    # problem_environments
    url(r'^problem_environments/$', ProblemEnvironmentListView.as_view(), name='problemenvironment-list'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/$', ProblemEnvironmentDetailView.as_view(), name='problemenvironment-detail'),
]
