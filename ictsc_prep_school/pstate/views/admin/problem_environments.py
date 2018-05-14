from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.problems import ProblemEnvironmentCreateExecuteForm, ProblemEnvironmentDestroyExecuteForm
from pstate.forms.problem_environments import ProblemEnvironmentForm, ProblemEnvironmentUpdateForm
from pstate.models import Problem, ProblemEnvironment, ProblemEnvironmentLog
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin


class ProblemEnvironmentCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ProblemEnvironmentForm
    template_name = 'admin_pages/common/add.html'
    success_url = "/manage/problem_environments/"

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
                                                 team=form.cleaned_data['team'],
                                                 participant=None,
                                                 environment=environment,
                                                 problem=problem)
        problem_environment.save()

        # VNCサーバのパスワードを参照しworkerに対して処理の実行命令する際に転送する.
        var = {"VNC_SERVER_PASSWORD": problem_environment.vnc_server_password}
        # workerに対して実行命令を発行.
        from terraform_manager.terraform_manager_tasks import direct_apply
        direct_apply.delay(environment.id, problem.terraform_file_id.id, var)
        ProblemEnvironmentLog(message="Creating problem environment started",
                              before_state=None,
                              after_state="IN_PREPARATION",
                              problem_environment=problem_environment).save()
        return HttpResponseRedirect(self.success_url + str(problem_environment.id))


class ProblemEnvironmentListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = ProblemEnvironment
    paginate_by = 15
    template_name = 'admin_pages/problem_environment/index.html'


class ProblemEnvironmentDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/detail.html'


class ProblemEnvironmentUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = ProblemEnvironment
    form_class = ProblemEnvironmentUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/problem_environments/'


class ProblemEnvironmentDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = ProblemEnvironment
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/problem_environments/'


class ProblemEnvironmentTestRunExecuteView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_create_execute.html'
    form_class = ProblemEnvironmentCreateExecuteForm
    success_url = "/manage/problem_environments/"

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

        # VNCサーバのパスワードを参照しworkerに対して処理の実行命令する際に転送する.
        var = {"VNC_SERVER_PASSWORD": problem_environment.vnc_server_password}
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
    success_url = "/manage/problems/"

    def form_valid(self, form):
        problem = Problem.objects.get(id=self.kwargs['pk'])
        # workerに対して処理の実行命令.
        from terraform_manager.models import Environment
        environment = Environment(terraform_file=problem.terraform_file_id,
                                  is_locked=False)
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


class ProblemEnvironmentDestroyView(LoginRequiredAndPermissionRequiredMixin, FormView):
    template_name = 'admin_pages/problem/problem_environment_destroy_execute.html'
    form_class = ProblemEnvironmentDestroyExecuteForm
    success_url = "/manage/problem_environments/"

    def form_valid(self, form):
        problem_environment = ProblemEnvironment.objects.get(id=self.kwargs['pk'])
        environment = problem_environment.environment
        # workerに対して処理の実行命令.
        from terraform_manager.terraform_manager_tasks import destroy
        var = []
        destroy.delay(environment.id, var)
        ProblemEnvironmentLog(message="Problem environment destroying started",
                              before_state=problem_environment.state,
                              after_state="WAITING_FOR_DELETE",
                              problem_environment=problem_environment).save()
        return HttpResponseRedirect(self.success_url + str(problem_environment.id))
