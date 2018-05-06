from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from pstate.models import Participant, Team

from pstate.forms.add_participant import ParticipantForm
from pstate.forms.add_team import TeamForm


def login(request):
    return render(request, 'admin_pages/auth/login.html')


#@login_required
def index(request):
    return render(request, 'admin_pages/index.html')


class ParticipantListView(ListView):

    model = Participant
    paginate_by = 100
    template_name = 'admin_pages/participant/index.html'

class ParticipantCreateView(CreateView):

    form_class = ParticipantForm
    template_name = 'admin_pages/participant/add.html'
    success_url = '/manage/participants/'


class TeamListView(ListView):

    model = Team
    paginate_by = 100
    template_name = 'admin_pages/team/index.html'


class TeamCreateView(CreateView):

    form_class = TeamForm
    template_name = 'admin_pages/team/add.html'
    success_url = '/manage/teams/'


class TeamDetailView(DetailView):

    model = Team
    template_name = 'admin_pages/team/detail.html'


class TeamUpdateView(UpdateView):

    model = Team
    fields = ['__all__']
    template_name = 'admin_pages/team/edit.html'
    success_url = '/manage/teams/'


class TeamDeleteView(DeleteView):

    model = Team
    template_name = 'admin_pages/team/delete.html'
    success_url = '/manage/teams/'
