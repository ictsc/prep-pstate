from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.teams import TeamForm, TeamUpdateForm, TeamBulkCreateForm
from pstate.models import Team, Github
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin


class TeamCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = TeamForm
    template_name = 'admin_pages/team/add.html'
    success_url = '/pstate/manage/teams/'


class TeamListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Team
    paginate_by = 100
    template_name = 'admin_pages/team/index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class TeamDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Team
    template_name = 'admin_pages/team/detail.html'


class TeamUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Team
    form_class = TeamUpdateForm
    template_name = 'admin_pages/team/edit.html'
    success_url = '/pstate/manage/teams/'


class TeamDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Team
    template_name = 'admin_pages/common/delete.html'
    success_url = '/pstate/manage/teams/'

class TeamBulkCreateView(LoginRequiredAndPermissionRequiredMixin, FormView):
    form_class = TeamBulkCreateForm
    template_name = 'admin_pages/team/bulk-add.html'
    success_url = '/pstate/manage/teams/'

    def form_valid(self, form):

        # Githubの情報を読み込む
        github = Github.objects.get(id=1)
        git_source = github.git_source
        ssh_private_key = github.ssh_private_key
        project_root_path = github.project_root_path
        teams_file = github.teams_file
        
        with open("key_file", mode="w") as f:
            f.write(ssh_private_key)

        import os
        os.chmod("key_file", 0o600)

        #リポジトリからClone
        from git import Repo
        ssh_cmd = 'ssh -i key_file'
        Repo.clone_from("git@github.com:ictsc/ictsc-sandbox.git", "./github_clone", env={'GIT_SSH_COMMAND': ssh_cmd})


        return HttpResponseRedirect(self.success_url)
