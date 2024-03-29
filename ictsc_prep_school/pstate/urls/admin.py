from celery.app.routes import Router
from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pstate.views.admin import index, dashboard, change_team_password, change_participant_password, close_window
from pstate.views.admin.api import ProblemEnvironmentViewSet
from pstate.views.admin.participants import ParticipantListView, ParticipantDetailView, ParticipantCreateView, \
    ParticipantUpdateView, ParticipantDeleteView
from pstate.views.admin.problem_environments import ProblemEnvironmentCreateView, ProblemEnvironmentTestRunExecuteView, \
    ProblemEnvironmentListView, ProblemEnvironmentDetailView, ProblemEnvironmentUpdateView, \
    ProblemEnvironmentDeleteView, ProblemEnvironmentDestroyView, ProblemEnvironmentRecreateView, \
    ProblemEnvironmentApplyView, ProblemEnvironmentBulkDestroyDeleteView
from pstate.views.admin.problems import ProblemListView, ProblemDetailView, ProblemCreateView, ProblemUpdateView, \
    ProblemDescriptionUpdateView, ProblemDeleteView, ProblemPreviewView, ProblemBulkCreateView, ProblemAllDeleteView
from pstate.views.admin.providers import ProviderListView, ProviderDetailView, ProviderCreateView, ProviderUpdateView, \
    ProviderDeleteView, AttributeListView, AttributeCreateView, AttributeUpdateView, AttributeDeleteView
from pstate.views.admin.teams import TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView, TeamDeleteView, \
    TeamBulkCreateView, TeamAllDeleteView
from pstate.views.admin.terraform_files import TerraformFileCreateView, TerraformFileUpdateView, VariableCreateView, \
    VariableUpdateView, VariableDeleteView, ShellScriptCreateView, ShellScriptUpdateView, ShellScriptDeleteView
from pstate.views.admin.github import GithubListView, GithubDetailView, GithubCreateView, \
    GithubUpdateView, GithubDeleteView


router = DefaultRouter()
router.register(r'problem_environments', ProblemEnvironmentViewSet, base_name='api')

app_name = 'pstate-manage'
urlpatterns = [
    path('', index, name='index'),
    path('dashboard', dashboard, name='dashboard'),
    # teams
    url(r'^teams/$', TeamListView.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^teams/add/$', TeamCreateView.as_view(), name='team-add'),
    url(r'^teams/bulk-add/$', TeamBulkCreateView.as_view(), name='bulk-team-add'),
    url(r'^teams/all-team-delete/$', TeamAllDeleteView.as_view(), name='all-team-delete'),
    url(r'^teams/(?P<pk>[0-9]+)/edit/$', TeamUpdateView.as_view(), name='team-edit'),
    url(r'^teams/(?P<pk>[0-9]+)/delete/$', TeamDeleteView.as_view(), name='team-delete'),
    url(r'^teams/(?P<pk>[0-9]+)/change_password/$', change_team_password, name='team-change_password'),
    # participants
    url(r'^participants/$', ParticipantListView.as_view(), name='participant-list'),
    url(r'^participants/(?P<pk>[0-9]+)/$', ParticipantDetailView.as_view(), name='participant-detail'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='participant-add'),
    url(r'^participants/(?P<pk>[0-9]+)/edit/$', ParticipantUpdateView.as_view(), name='participant-edit'),
    url(r'^participants/(?P<pk>[0-9]+)/delete/$', ParticipantDeleteView.as_view(), name='participant-delete'),
    url(r'^participants/(?P<pk>[0-9]+)/change_password/$', change_participant_password, name='participant-change_password'),
    # problems
    url(r'^problems/$', ProblemListView.as_view(), name='problem-list'),
    url(r'^problems/(?P<pk>[0-9]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^problems/(?P<pk>[0-9]+)/preview/$', ProblemPreviewView.as_view(), name='problem-preview'),
    url(r'^problems/add/$', ProblemCreateView.as_view(), name='problem-create'),
    url(r'^problems/bulk-add/$', ProblemBulkCreateView.as_view(), name='bulk-problem-add'),
    url(r'^problems/all-team-delete/$', ProblemAllDeleteView.as_view(), name='all-problem-delete'),
    url(r'^problems/(?P<pk>[0-9]+)/edit/$', ProblemUpdateView.as_view(), name='problem-edit'),
    url(r'^problems/(?P<pk>[0-9]+)/body/edit/$', ProblemDescriptionUpdateView.as_view(), name='problem-body-edit'),
    url(r'^problems/(?P<pk>[0-9]+)/delete/$', ProblemDeleteView.as_view(), name='problem-delete'),
    url(r'^problems/(?P<pk>[0-9]+)/problem_environment/add/$', ProblemEnvironmentCreateView.as_view(), name='problems-problemenvironment-create'),
    url(r'^problems/(?P<pk>[0-9]+)/problem_environment/test_run/$', ProblemEnvironmentTestRunExecuteView.as_view(), name='problems-problemenvironment-test_run'),
    # terraformfiles
    url(r'^problems/(?P<pk>[0-9]+)/terraform_file/add/$', TerraformFileCreateView.as_view(), name='terraformfile-create'),
    url(r'^terraform_files/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/edit/$', TerraformFileUpdateView.as_view(), name='terraformfile-edit'),
    # variables
    url(r'^problems/(?P<pk>[0-9]+)/variable/add/$', VariableCreateView.as_view(), name='variable-create'),
    url(r'^terraform_file/variables(?P<pk>[0-9]+)/edit/$', VariableUpdateView.as_view(), name='variable-edit'),
    url(r'^terraform_file/variables/(?P<pk>[0-9]+)/delete/$', VariableDeleteView.as_view(), name='variable-delete'),
    # shell scripts
    url(r'^problems/(?P<pk>[0-9]+)/shell_script/add/$', ShellScriptCreateView.as_view(), name='shell_script-create'),
    url(r'^shell_scripts/(?P<pk>[0-9]+)/edit/$', ShellScriptUpdateView.as_view(), name='shell_script-edit'),
    url(r'^shell_scripts/(?P<pk>[0-9]+)/delete/$', ShellScriptDeleteView.as_view(), name='shell_script-delete'),
    # problem_environments
    url(r'^problem_environments/$', ProblemEnvironmentListView.as_view(), name='problemenvironment-list'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/$', ProblemEnvironmentDetailView.as_view(), name='problemenvironment-detail'),
    url(r'^problem_environments/add/$', ProblemEnvironmentCreateView.as_view(), name='problemenvironment-create'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/edit/$', ProblemEnvironmentUpdateView.as_view(), name='problemenvironment-edit'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/delete/$', ProblemEnvironmentDeleteView.as_view(), name='problemenvironment-delete'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/apply/$', ProblemEnvironmentApplyView.as_view(), name='problemenvironment-apply'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/destroy/$', ProblemEnvironmentDestroyView.as_view(), name='problemenvironment-destroy'),
    url(r'^problem_environments/(?P<pk>[0-9]+)/recreate/$', ProblemEnvironmentRecreateView.as_view(), name='problemenvironment-recreate'),
     url(r'^problem_environments/bulk_destroy_delete/$', ProblemEnvironmentBulkDestroyDeleteView.as_view(), name='problemenvironment-bulk-destroy'),
    # setting/providers
    url(r'^setting/providers/$', ProviderListView.as_view(), name='provider-list'),
    url(r'^setting/providers/(?P<pk>[0-9]+)/$', ProviderDetailView.as_view(), name='provider-detail'),
    url(r'^setting/providers/add/$', ProviderCreateView.as_view(), name='provider-create'),
    url(r'^setting/providers/(?P<pk>[0-9]+)/edit/$', ProviderUpdateView.as_view(), name='provider-edit'),
    url(r'^setting/providers/(?P<pk>[0-9]+)/delete/$', ProviderDeleteView.as_view(), name='provider-delete'),
    # setting/attributes
    url(r'^setting/attributes/$', AttributeListView.as_view(), name='attribute-list'),
    url(r'^setting/attributes/add/$', AttributeCreateView.as_view(), name='attribute-create'),
    url(r'^setting/attributes/(?P<pk>[0-9]+)/edit/$', AttributeUpdateView.as_view(), name='attribute-edit'),
    url(r'^setting/attributes/(?P<pk>[0-9]+)/delete/$', AttributeDeleteView.as_view(), name='attribute-delete'),
    # setting/github
    url(r'^setting/github/$', GithubListView.as_view(), name='github-list'),
    url(r'^setting/github/(?P<pk>[0-9]+)/$', GithubDetailView.as_view(), name='github-detail'),
    url(r'^setting/github/add/$', GithubCreateView.as_view(), name='github-create'),
    url(r'^setting/github/(?P<pk>[0-9]+)/edit/$', GithubUpdateView.as_view(), name='github-edit'),
    url(r'^setting/github/(?P<pk>[0-9]+)/delete/$', GithubDeleteView.as_view(), name='github-delete'),
    # util
    url(r'^close_window/$', close_window, name='window-close'),
    # API
    url(r'^api/', include(router.urls))
]
