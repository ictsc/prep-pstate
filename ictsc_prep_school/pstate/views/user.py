from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, FormView

from pstate.models import Problem, ProblemEnvironment

from pstate.forms.add_problem import ProblemEnvironmentCreateExecuteForm


@login_required
def index(request):
    return render(request, 'user_pages/index.html')


@login_required
def dashboard(request):
    return render(request, 'user_pages/dashboard.html')


class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    paginate_by = 100
    #   FIXME   :   fix template_name file path
    template_name = 'user_pages/problem/index.html'

    def get_queryset(self):
        return Problem.objects.filter(is_enabled=True)


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    paginate_by = 100
    #   FIXME   :   fix template_name file path
    template_name = 'user_pages/problem/detail.html'

    def get_queryset(self):
        return Problem.objects.filter(is_enabled=True)


class ProblemEnvironmentListView(LoginRequiredMixin, ListView):
    model = ProblemEnvironment
    paginate_by = 100
    #   FIXME   :   fix template_name file path
    template_name = 'user_pages/problem_environment/index.html'

    def get_queryset(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return ProblemEnvironment.objects.filter(team=Team.objects.get(id=self.request.user.id))
        else:
            from pstate.models import Participant
            return ProblemEnvironment.objects.filter(participant=Participant.objects.get(id=self.request.user.id))


class ProblemEnvironmentDetailView(LoginRequiredMixin, DetailView):
    model = ProblemEnvironment
    paginate_by = 100
    #   FIXME   :   fix template_name file path
    template_name = 'user_pages/problem_environment/detail.html'

    def get_queryset(self):
        if self.request.user.is_team:
            from pstate.models import Team
            return ProblemEnvironment.objects.filter(team=Team.objects.get(id=self.request.user.id))
        else:
            from pstate.models import Participant
            return ProblemEnvironment.objects.filter(participant=Participant.objects.get(id=self.request.user.id))


class ProblemEnvironmentCreateView(LoginRequiredMixin, CreateView):
    #   FIXME   :   fix template_name file path
    # form_class = ProblemEnvironmentForm
    #   FIXME   :   fix template_name file path
    template_name = 'user_pages/problem_environment/add.html'
    #   FIXME   :   fix template_name file path
    success_url = "/user/problem_environments/"


class ProblemEnvironmentCreateExecuteView(LoginRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_create_execute.html'
    form_class = ProblemEnvironmentCreateExecuteForm
    success_url = "/manage/problems/"

    def form_valid(self, form):
        problem = Problem.objects.get(id=self.kwargs['pk'])
        # workerに対して処理の実行命令.
        from terraform_manager.models import Environment
        environment = Environment(terraform_file=problem.terraform_file_id,
                                  locked=False)
        environment.save()

        from terraform_manager.terraform_manager_tasks import direct_apply
        var = []
        direct_apply.delay(environment.id, problem.terraform_file_id.id, var)

        # データの作成.
        problem_environment = ProblemEnvironment(vnc_server_ipv4_address=None,
                                                 is_enabled=True,
                                                 # teamもしくはparticipantが必ず指定される.
                                                 team=None,
                                                 participant=None,
                                                 environment=environment,
                                                 problem=problem)
        problem_environment.save()
        return HttpResponseRedirect(self.success_url)
