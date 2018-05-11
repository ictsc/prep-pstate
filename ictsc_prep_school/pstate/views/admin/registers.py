from django.views.generic import CreateView

from pstate.forms.participants import ParticipantRegisterForm
from pstate.forms.teams import TeamRegisterForm


class TeamRegisterView(CreateView):
    form_class = TeamRegisterForm
    template_name = 'user_pages/common/register_team.html'
    success_url = '/user'


class ParticipantRegisterView(CreateView):
    form_class = ParticipantRegisterForm
    template_name = 'user_pages/common/register_participant.html'
    success_url = '/user'
