from django.conf.urls import url
from django.urls import path

from pstate import views

from pstate.views import ParticipantListView, ParticipantCreateView,\
    TeamListView, TeamCreateView, TeamDetailView, TeamUpdateView, TeamDeleteView,\
    ParticipantUpdateView, ParticipantDeleteView,\
    ProblemListView, ProblemDetailView, ProblemCreateView,\
    ProblemEnvironmentListView, ProblemEnvironmentDetailView, ProblemEnvironmentCreateView, ProblemEnvironmentUpdateView, ProblemEnvironmentDeleteView

from pstate.views import ProviderListView, ProviderDetailView, ProviderCreateView, ProviderUpdateView, \
    ProviderDeleteView, ProblemUpdateView, ProblemDeleteView

from pstate.views import TerraformFileCreateView

from pstate.views import ProblemEnvironmentCreateExecuteView

from pstate.views import AttributeListView, AttributeCreateView, AttributeUpdateView, \
    AttributeDeleteView

from pstate.views import ProblemDescriptionUpdateView

from pstate.views import TerraformFileUpdateView

from pstate.views import ShellScriptUpdateView, ShellScriptCreateView

from pstate.views import ShellScriptDeleteView

from pstate.views import VariableCreateView, VariableUpdateView, VariableDeleteView

app_name = 'pstate-manage'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    # teams
    url(r'^teams/$', TeamListView.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(), name='team-detail'),
    url(r'^teams/add/$', TeamCreateView.as_view(), name='team-add'),
    url(r'^teams/(?P<pk>[0-9]+)/edit/$', TeamUpdateView.as_view(), name='team-edit'),
    url(r'^teams/(?P<pk>[0-9]+)/delete/$', TeamDeleteView.as_view(), name='team-delete'),
    url(r'^teams/(?P<pk>[0-9]+)/change_password/$', views.change_team_password, name='team-change_password'),
    # participants
    url(r'^participants/$', ParticipantListView.as_view(), name='participant-list'),
    url(r'^participants/(?P<pk>[0-9]+)/$', views.ParticipantDetailView.as_view(), name='participant-detail'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='participant-add'),
    url(r'^participants/(?P<pk>[0-9]+)/edit/$', views.ParticipantUpdateView.as_view(), name='participant-edit'),
    url(r'^participants/(?P<pk>[0-9]+)/delete/$', views.ParticipantDeleteView.as_view(), name='participant-delete'),
    url(r'^participants/(?P<pk>[0-9]+)/change_password/$', views.change_participant_password, name='participant-change_password'),
    # problems
    url(r'^problems/$', ProblemListView.as_view(), name='problem-list'),
    url(r'^problems/(?P<pk>[0-9]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^problems/add/$', ProblemCreateView.as_view(), name='problem-create'),
    url(r'^problems/(?P<pk>[0-9]+)/edit/$', ProblemUpdateView.as_view(), name='problem-edit'),
    url(r'^problems/(?P<pk>[0-9]+)/body/edit/$', ProblemDescriptionUpdateView.as_view(), name='problem-body-edit'),
    url(r'^problems/(?P<pk>[0-9]+)/delete/$', ProblemDeleteView.as_view(), name='problem-delete'),
    url(r'^problems/(?P<pk>[0-9]+)/problem_environment/add/$', ProblemEnvironmentCreateExecuteView.as_view(), name='problems-problemenvironment-create'),
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
    # util
    url(r'^close_window/$', views.close_window, name='window-close'),
]
