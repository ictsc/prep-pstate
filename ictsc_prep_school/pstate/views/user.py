from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView

from pstate.forms.problems import ProblemStartForm
from pstate.models import Problem, ProblemEnvironment, ProblemEnvironmentLog

from pstate.forms.change_password import NoOlbPasswordCheckPasswordChangeForm
from pstate.models import Team

from pstate.forms.teams import TeamUserUpdateForm


@login_required
def change_password(request):
    if request.method == 'POST':
        form = NoOlbPasswordCheckPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('pstate-user:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
def index(request):
    return render(request, 'user_pages/index.html')


@login_required
def dashboard(request):
    return render(request, 'user_pages/dashboard.html')


class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    paginate_by = 100
    template_name = 'user_pages/problem/index.html'

    def get_queryset(self):
        return Problem.objects.filter(is_enabled=True)


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = 'user_pages/problem/detail.html'

    def get_queryset(self):
        return Problem.objects.filter(is_enabled=True)


class ProblemEnvironmentListView(LoginRequiredMixin, ListView):
    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'user_pages/problem_environment/index.html'

    def get_queryset(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return ProblemEnvironment.objects.filter(team=Team.objects.get(id=self.request.user.id),
                                                     is_enabled=True,
                                                     problem__is_enabled=True)
        else:
            from pstate.models import Participant
            return ProblemEnvironment.objects.filter(participant=Participant.objects.get(id=self.request.user.id),
                                                     is_enabled=True,
                                                     problem__is_enabled=True)


class ProblemEnvironmentDetailView(LoginRequiredMixin, DetailView):
    model = ProblemEnvironment
    template_name = 'user_pages/problem_environment/detail.html'

    def get_queryset(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return ProblemEnvironment.objects.filter(team=Team.objects.get(id=self.request.user.id))
        else:
            from pstate.models import Participant
            return ProblemEnvironment.objects.filter(participant=Participant.objects.get(id=self.request.user.id))


class ProblemStartView(LoginRequiredMixin, FormView):
    template_name = 'user_pages/problem/start.html'
    form_class = ProblemStartForm
    success_url = "/user/problem_environments/"

    def form_valid(self, form):
        # TODO: ログインしているユーザでpostしているかを確認する.
        problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        problem_environment.state = "IN_PROGRESS"
        problem_environment.save(message="To start solving problems")
        return HttpResponseRedirect(self.success_url + str(self.kwargs['pk']))


class ProblemEndView(LoginRequiredMixin, FormView):
    template_name = 'user_pages/problem/end.html'
    form_class = ProblemStartForm
    success_url = "/user/problem_environments/"

    def form_valid(self, form):
        # TODO: ログインしているユーザでpostしているかを確認する.
        problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        problem_environment.state = "FINISH"
        problem_environment.save(message="Finish solving the problem")
        return HttpResponseRedirect(self.success_url + str(self.kwargs['pk']))


class TeamDetailView(LoginRequiredMixin, ListView):
    model = Team
    paginate_by = 1
    template_name = 'user_pages/team/detail.html'

    def get_queryset(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return Team.objects.filter(id=self.request.user.id)
        else:
            return Team.objects.none()


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamUserUpdateForm
    template_name = 'user_pages/team/edit.html'
    success_url = '/user/team/'

    def get_object(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return Team.objects.get(id=self.request.user.id)
        else:
            return Team.objects.none()
