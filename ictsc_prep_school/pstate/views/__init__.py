from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from pstate.models import Participant, Team, Problem, ProblemEnvironment

from pstate.forms.add_participant import ParticipantForm
from pstate.forms.add_team import TeamForm
from pstate.forms.add_problem import ProblemForm
from pstate.forms.add_problemenvironment import ProblemEnvironmentForm
from pstate.forms.add_provider import ProviderForm

from terraform_manager.models import Provider

from pstate.forms.add_terraformfile import TerraformFileForm

from pstate.forms.add_problem import ProblemEnvironmentCreateExecuteForm

from pstate.forms.change_password import NoOlbPasswordCheckPasswordChangeForm

from pstate.forms.add_participant import ParticipantUpdateForm

from pstate.forms.add_team import TeamUpdateForm

from pstate.forms.add_participant import ParticipantRegisterForm
from pstate.forms.add_team import TeamRegisterForm

from terraform_manager.models import Attribute

from pstate.forms.add_problem import ProblemDescriptionUpdateForm

from terraform_manager.models import TerraformFile

from pstate.forms.add_terraformfile import  TerraformFileUpdateForm

from pstate.forms.add_shell_script import ShellScriptForm, ShellScriptUpdateForm
from terraform_manager.models import ShellScript


def login(request):
    return render(request, 'admin_pages/auth/login.html')


@login_required
def logout(request):
    return render(request, 'admin_pages/auth/logout.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = NoOlbPasswordCheckPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
def change_team_password(request, pk):
    if request.method == 'POST':
        user = Team.objects.get(id=pk)
        form = NoOlbPasswordCheckPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


def change_participant_password(request, pk):
    if request.method == 'POST':
        user = Participant.objects.get(id=pk)
        form = NoOlbPasswordCheckPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
def index(request):
    return render(request, 'admin_pages/index.html')


@login_required
def dashboard(request):
    return render(request, 'admin_pages/dashboard.html')


def close_window(request):
    return render(request, 'admin_pages/common/close.html')


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    paginate_by = 100
    template_name = 'admin_pages/participant/index.html'


class ParticipantCreateView(LoginRequiredMixin, CreateView):
    form_class = ParticipantForm
    template_name = 'admin_pages/participant/add.html'
    success_url = '/manage/participants/'


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    paginate_by = 100
    template_name = 'admin_pages/team/index.html'


class TeamCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamForm
    template_name = 'admin_pages/team/add.html'
    success_url = '/manage/teams/'


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'admin_pages/team/detail.html'


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamUpdateForm
    template_name = 'admin_pages/team/edit.html'
    success_url = '/manage/teams/'


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/teams/'


class ParticipantDetailView(LoginRequiredMixin, DetailView):
    model = Participant
    template_name = 'admin_pages/participant/detail.html'


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = Participant
    form_class = ParticipantUpdateForm
    template_name = 'admin_pages/participant/edit.html'
    success_url = '/manage/participants/'


class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/participants/'


class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/index.html'


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/detail.html'


class ProblemCreateView(LoginRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = 'admin_pages/problem/add.html'
    success_url = "/manage/problems/"


class ProblemUpdateView(LoginRequiredMixin, UpdateView):
    model = ProblemForm
    fields = '__all__'
    template_name = 'admin_pages/problem/edit.html'
    success_url = '/manage/problems/'


class ProblemDescriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemDescriptionUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        form.save(commit=True)
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/problems/'


class ProblemEnvironmentListView(LoginRequiredMixin, ListView):
    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/index.html'


class ProblemEnvironmentDetailView(LoginRequiredMixin, DetailView):
    model = ProblemEnvironment
    paginate_by = 100
    template_name = 'admin_pages/problem_environment/detail.html'


class ProblemEnvironmentCreateView(LoginRequiredMixin, CreateView):
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
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/problem_environments/'


class ProviderListView(LoginRequiredMixin, ListView):
    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/index.html'


class ProviderDetailView(LoginRequiredMixin, DetailView):
    model = Provider
    paginate_by = 100
    template_name = 'admin_pages/setting/provider/detail.html'


class ProviderCreateView(LoginRequiredMixin, CreateView):
    form_class = ProviderForm
    template_name = 'admin_pages/setting/provider/add.html'
    success_url = "/manage/setting/providers/"


class ProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = Provider
    fields = ('__all__')
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/setting/providers/'


class ProviderDeleteView(LoginRequiredMixin, DeleteView):
    model = Provider
    template_name = 'admin_pages/setting/provider/delete.html'
    success_url = '/manage/setting/providers/'


class TerraformFileCreateView(LoginRequiredMixin, CreateView):
    form_class = TerraformFileForm
    template_name = 'admin_pages/terraform_file/add.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        terraform_file = form.save(commit=True)
        problem = Problem.objects.get(id=self.kwargs['pk'])
        problem.terraform_file_id = terraform_file
        problem.save()
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class TerraformFileUpdateView(LoginRequiredMixin, UpdateView):
    model = TerraformFile
    form_class = TerraformFileUpdateForm
    template_name = 'admin_pages/terraform_file/edit.html'

    def form_valid(self, form):
        form.save(commit=True)
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


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


class TeamRegisterView(CreateView):
    form_class = TeamRegisterForm
    template_name = 'user_pages/common/register_team.html'
    success_url = '/user'


class ParticipantRegisterView(CreateView):
    form_class = ParticipantRegisterForm
    template_name = 'user_pages/common/register_participant.html'
    success_url = '/user'


class AttributeListView(LoginRequiredMixin, ListView):
    model = Attribute
    paginate_by = 100
    template_name = 'admin_pages/setting/attribute/index.html'


class AttributeCreateView(LoginRequiredMixin, CreateView):
    model = Attribute
    fields = '__all__'
    template_name = 'admin_pages/setting/attribute/add.html'
    success_url = '/manage/setting/attributes'


class AttributeUpdateView(LoginRequiredMixin, UpdateView):
    model = Attribute
    fields = '__all__'
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/setting/attributes'


class AttributeDeleteView(LoginRequiredMixin, DeleteView):
    model = Attribute
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/setting/attributes'


class ShellScriptCreateView(LoginRequiredMixin, CreateView):
    form_class = ShellScriptForm
    template_name = 'admin_pages/terraform_file/add.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        shell_script = form.save(commit=False)
        problem = Problem.objects.get(id=self.kwargs['pk'])
        shell_script.terraform_file = problem.terraform_file_id
        shell_script.save()
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ShellScriptUpdateView(LoginRequiredMixin, UpdateView):
    model = ShellScript
    form_class = ShellScriptUpdateForm
    template_name = 'admin_pages/terraform_file/edit.html'

    def form_valid(self, form):
        form.save(commit=True)
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ShellScriptDeleteView(LoginRequiredMixin, DeleteView):
    model = ShellScript
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/close_window/'
