from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from pstate.models import Participant, Team, Problem, ProblemEnvironment

from pstate.forms.add_participant import ParticipantForm
from pstate.forms.add_team import TeamForm
from pstate.forms.add_problem import ProblemForm
from pstate.forms.add_problemenvironment import ProblemEnvironmentForm
from pstate.forms.add_provider import ProviderForm

from terraform_manager.models import Provider


def login(request):
    return render(request, 'admin_pages/auth/login.html')


#@login_required
def index(request):
    return render(request, 'admin_pages/index.html')


def dashboard(request):
    return render(request, 'admin_pages/dashboard.html')


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
    form_class = TeamForm
    template_name = 'admin_pages/team/edit.html'
    success_url = '/manage/teams/'


class TeamDeleteView(DeleteView):

    model = Team
    template_name = 'admin_pages/team/delete.html'
    success_url = '/manage/teams/'


class ParticipantDetailView(DetailView):

    model = Participant
    template_name = 'admin_pages/participant/detail.html'


class ParticipantUpdateView(UpdateView):

    model = Participant
    fields = ('__all__')
    template_name = 'admin_pages/participant/edit.html'
    success_url = '/manage/participants/'

class ParticipantDeleteView(DeleteView):

    model = Participant
    template_name = 'admin_pages/participant/delete.html'
    success_url = '/manage/participants/'


class ProblemListView(ListView):

    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/index.html'


class ProblemDetailView(DetailView):

    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/detail.html'


class ProblemCreateView(CreateView):

    form_class = ProblemForm
    template_name = 'admin_pages/problem/add.html'
    success_url = "/manage/problems/"


class ProblemEnvironmentListView(ListView):

    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/index.html'


class ProblemEnvironmentDetailView(DetailView):

    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/detail.html'


class ProblemEnvironmentCreateView(CreateView):

    form_class = ProblemEnvironmentForm
    template_name = 'admin_pages/problem_environment/add.html'
    success_url = "/manage/problem_environments/"


class ProblemEnvironmentUpdateView(UpdateView):

    model = ProblemEnvironment
    fields = ('__all__')
    template_name = 'admin_pages/problem_environment/edit.html'
    success_url = '/manage/problem_environments/'


class ProblemEnvironmentDeleteView(DeleteView):

    model = ProblemEnvironment
    template_name = 'admin_pages/problem_environment/delete.html'
    success_url = '/manage/problem_environments/'


class ProviderListView(ListView):

    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/index.html'


class ProviderDetailView(DetailView):

    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/detail.html'


class ProviderCreateView(CreateView):

    form_class = ProviderForm
    template_name = 'admin_pages/setting/provider/add.html'
    success_url = "/manage/setting/providers/"


class ProviderUpdateView(UpdateView):

    model = Provider
    fields = ('__all__')
    template_name = 'admin_pages/setting/provider/edit.html'
    success_url = '/manage/setting/providers/'


class ProviderDeleteView(DeleteView):

    model = Provider
    template_name = 'admin_pages/setting/provider/delete.html'
    success_url = '/manage/setting/providers/'
