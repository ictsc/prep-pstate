from django.views.generic import CreateView

from pstate.forms.add_participant import ParticipantRegisterForm
from pstate.forms.add_team import TeamRegisterForm


class TeamRegisterView(CreateView):
    form_class = TeamRegisterForm
    template_name = 'user_pages/common/register_team.html'
    success_url = '/user'


class ParticipantRegisterView(CreateView):
    form_class = ParticipantRegisterForm
    template_name = 'user_pages/common/register_participant.html'
    success_url = '/user'
