from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.problems import ProblemEnvironmentCreateExecuteForm, ProblemEnvironmentDestroyExecuteForm, \
    ProblemEnvironmentRecreateExecuteForm, ProblemEnvironmentBulkDestroyDeleteExecuteForm
from pstate.forms.problem_environments import ProblemEnvironmentForm, ProblemEnvironmentUpdateForm
from pstate.models import Problem, ProblemEnvironment, ProblemEnvironmentLog, Team, NotificationQueue
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from django.shortcuts import render

class ProblemEnvironmentCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ProblemEnvironmentForm
    template_name = 'admin_pages/problem_environment/add.html'
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):
        problem = Problem.objects.get(id=self.kwargs['pk'])
        for team in form.cleaned_data['teams']:
            # workerに対して処理の実行命令.
            from terraform_manager.models import Environment
            environment = Environment(terraform_file=problem.terraform_file_id,
                                      is_locked=False)
            environment.save()

            # データの作成.
            problem_environment = ProblemEnvironment(vnc_server_ipv4_address=None,
                                                     is_enabled=True,
                                                     team=team,
                                                     participant=None,
                                                     environment=environment,
                                                     problem=problem)
            problem_environment.save()
            NotificationQueue.objects.create(environment=environment)

            # VNCサーバのパスワードを参照しworkerに対して処理の実行命令する際に転送する.
            var = {"VNC_SERVER_PASSWORD": problem_environment.vnc_server_password,
                   "TEAM_LOGIN_ID": team.username}
            # workerに対して実行命令を発行.
            from terraform_manager.terraform_manager_tasks import direct_apply
            direct_apply.delay(environment.id, problem.terraform_file_id.id, var)
            ProblemEnvironmentLog(message="Creating problem environment started",
                                  before_state=None,
                                  after_state="IN_PREPARATION",
                                  problem_environment=problem_environment).save()
        return HttpResponseRedirect(self.success_url)


class ProblemEnvironmentListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = ProblemEnvironment
    paginate_by = 15
    template_name = 'admin_pages/problem_environment/index.html'
    success_url = '/pstate/manage/problem_environments/'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get("ip_address") or self.request.GET.getlist("team") or self.request.GET.getlist("problem"):
            # 絞り込みした件数を全数表示.
            self.paginate_by = 1000
        teams = self.request.GET.getlist("team")
        problems = self.request.GET.getlist("problem")
        ipv4_address = self.request.GET.get("ip_address")
        if len(teams) != 0:
            queryset = queryset.filter(team__in=teams).order_by('id')
        if len(problems) != 0:
            queryset = queryset.filter(problem__in=problems).order_by('id')
        if self.request.GET.get("ip_address") is not None and not self.request.GET.get("ip_address") == "":
            queryset = queryset.filter(vnc_server_ipv4_address=ipv4_address)
        queryset = queryset.filter().order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Problem.objects.all()
        context['teams'] = Team.objects.all()
        return context

    def post(self, request):
        template_name = '/pstate/manage/problem_environments/bulk_destroy_delete/'
        response = HttpResponseRedirect(template_name)
        post_params = request.POST.urlencode()
        response['location'] += '?'+ post_params
        return response

class ProblemEnvironmentDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/detail.html'


class ProblemEnvironmentUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = ProblemEnvironment
    form_class = ProblemEnvironmentUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/problem_environments/'

    def get_success_url(self, **kwargs):
        return self.success_url + str(self.object.id)


class ProblemEnvironmentDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = ProblemEnvironment
    template_name = 'admin_pages/common/delete.html'
    success_url = '/pstate/manage/problem_environments/'


class ProblemEnvironmentTestRunExecuteView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_create_execute.html'
    form_class = ProblemEnvironmentCreateExecuteForm
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):
        problem = Problem.objects.get(id=self.kwargs['pk'])
        from terraform_manager.models import Environment
        environment = Environment(terraform_file=problem.terraform_file_id,
                                  is_locked=False)
        environment.save()

        # データの作成.
        problem_environment = ProblemEnvironment(vnc_server_ipv4_address=None,
                                                 is_enabled=True,
                                                 # teamもしくはparticipantが必ず指定される.
                                                 team=None,
                                                 participant=None,
                                                 environment=environment,
                                                 problem=problem)
        problem_environment.save()
        NotificationQueue.objects.create(environment=environment)

        # VNCサーバのパスワードを参照しworkerに対して処理の実行命令する際に転送する.
        var = {"VNC_SERVER_PASSWORD": problem_environment.vnc_server_password,
               "TEAM_LOGIN_ID": "ICTSC-ADMIN"}
        # workerに対して実行命令を発行.
        from terraform_manager.terraform_manager_tasks import direct_apply
        direct_apply.delay(environment.id, problem.terraform_file_id.id, var)
        ProblemEnvironmentLog(message="Creating problem environment started",
                              before_state=None,
                              after_state="IN_PREPARATION",
                              problem_environment=problem_environment).save()
        return HttpResponseRedirect(self.success_url + str(problem_environment.id))


class ProblemEnvironmentCreateExecuteView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_create_execute.html'
    form_class = ProblemEnvironmentCreateExecuteForm
    success_url = "/pstate/manage/problems/"

    def form_valid(self, form):
        problem = Problem.objects.get(id=self.kwargs['pk'])
        # workerに対して処理の実行命令.
        from terraform_manager.models import Environment
        environment = Environment(terraform_file=problem.terraform_file_id,
                                  is_locked=False)
        environment.save()

        # データの作成.
        problem_environment = ProblemEnvironment(vnc_server_ipv4_address=None,
                                                 is_enabled=True,
                                                 # teamもしくはparticipantが必ず指定される.
                                                 team=None,
                                                 participant=None,
                                                 environment=environment,
                                                 problem=problem)
        problem_environment.save()
        NotificationQueue.objects.create(environment=environment)

        from terraform_manager.terraform_manager_tasks import direct_apply
        var = []
        direct_apply.delay(environment.id, problem.terraform_file_id.id, var)
        return HttpResponseRedirect(self.success_url)


class ProblemEnvironmentApplyView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_apply_execute.html'
    form_class = ProblemEnvironmentDestroyExecuteForm
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):
        problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        environment = problem_environment.environment
        # workerに対して処理の実行命令.
        from terraform_manager.terraform_manager_tasks import apply

        var = {"VNC_SERVER_PASSWORD": problem_environment.vnc_server_password,
               "TEAM_LOGIN_ID": problem_environment.team.username}
        apply.delay(environment.id, var)

        ProblemEnvironmentLog(message="Problem environment reapplying started",
                              before_state=problem_environment.state,
                              after_state="IN_PREPARATION",
                              problem_environment=problem_environment).save()
        return HttpResponseRedirect(self.success_url + str(problem_environment.id))


class ProblemEnvironmentDestroyView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_destroy_execute.html'
    form_class = ProblemEnvironmentDestroyExecuteForm
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):
        problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        environment = problem_environment.environment
        # workerに投げる    
        self.terraform_destroy(problem_environment, environment)
        return HttpResponseRedirect(self.success_url + str(problem_environment.id))

    # workerに対して処理の実行命令.
    def terraform_destroy(self, problem_environment, environment):
        from terraform_manager.terraform_manager_tasks import destroy
        var = []
        destroy.delay(environment.id, var)
        ProblemEnvironmentLog(message="Problem environment destroying started",
                              before_state=problem_environment.state,
                              after_state="WAITING_FOR_DELETE",
                              problem_environment=problem_environment).save()



class ProblemEnvironmentRecreateView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem_environment/recreate.html'
    form_class = ProblemEnvironmentRecreateExecuteForm
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):
        destroy_problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        recreate_problem = destroy_problem_environment.problem
        target_team = destroy_problem_environment.team

        # 破棄処理.
        from terraform_manager.terraform_manager_tasks import destroy
        var = []
        destroy.delay(destroy_problem_environment.environment.id, var)

        ProblemEnvironmentLog(message="Problem environment destroying started",
                              before_state=destroy_problem_environment.state,
                              after_state="WAITING_FOR_DELETE",
                              problem_environment=destroy_problem_environment).save()

        # 破棄した問題環境の有効状態を無効にする.
        destroy_problem_environment.is_enabled = False
        destroy_problem_environment.save()

        # 再作成処理.
        from terraform_manager.models import Environment
        recreate_environment = Environment(terraform_file=recreate_problem.terraform_file_id, is_locked=False)
        recreate_environment.save()

        recreate_problem_environment = ProblemEnvironment(vnc_server_ipv4_address=None,
                                                          is_enabled=True,
                                                          team=target_team,
                                                          participant=None,
                                                          environment=recreate_environment,
                                                          problem=recreate_problem)
        recreate_problem_environment.save()
        NotificationQueue.objects.create(environment=recreate_environment)

        # VNCサーバのパスワードを参照しworkerに対して処理の実行命令する際に転送する.
        var = {"VNC_SERVER_PASSWORD": recreate_problem_environment.vnc_server_password,
               "TEAM_LOGIN_ID": target_team.username}

        from terraform_manager.terraform_manager_tasks import direct_apply
        direct_apply.delay(recreate_environment.id, recreate_problem.terraform_file_id.id, var)
        ProblemEnvironmentLog(message="Creating problem environment started",
                              before_state=None,
                              after_state="IN_PREPARATION",
                              problem_environment=recreate_problem_environment).save()
        return HttpResponseRedirect(self.success_url + str(recreate_problem_environment.id))

class ProblemEnvironmentBulkDestroyDeleteView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_bulk_destroy_execute.html'
    form_class = ProblemEnvironmentBulkDestroyDeleteExecuteForm
    success_url = "/pstate/manage/problem_environments/"

    def form_valid(self, form):

        post_pks = self.request.GET.getlist('problem_id')
        for problem_environment in ProblemEnvironment.objects.filter(pk__in=post_pks):
            environment = problem_environment.environment
            ProblemEnvironmentDestroyView().terraform_destroy(problem_environment, environment)
        if "delete" in self.request.GET:
            ProblemEnvironment.objects.filter(pk__in=post_pks).delete()
        return HttpResponseRedirect(self.success_url)