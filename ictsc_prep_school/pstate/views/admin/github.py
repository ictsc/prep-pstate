from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from pstate.forms.github import GithubForm, GithubUpdateForm
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from pstate.models import Github
from django.http import HttpResponseRedirect

class GithubCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = GithubForm
    template_name = 'admin_pages/setting/github/add.html'
    success_url = "/pstate/manage/setting/github/"


class GithubListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Github
    paginate_by = 100
    template_name = 'admin_pages/setting/github/index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class GithubDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Github
    paginate_by = 100
    template_name = 'admin_pages/setting/github/detail.html'


class GithubUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Github
    form_class = GithubUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/setting/github/'

    def get_success_url(self, **kwargs):
        return self.success_url + str(self.object.id)

class GithubDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Github
    template_name = 'admin_pages/setting/github/delete.html'
    success_url = '/pstate/manage/setting/github/'

def GithubRepoPullExecute(github):

    # Githubの情報を読み込む
    git_source = github.git_source
    ssh_private_key = github.ssh_private_key
    project_root_path = github.project_root_path
    teams_file = github.teams_file

    with open("key_file", mode="w", newline="\n") as f:
        f.write(ssh_private_key)

    import os
    os.chmod("key_file", 0o600)
    
    from git import Repo
    ssh_cmd = 'ssh -i key_file'
    #初回はリポジトリからClone、それ以降Pullする
    
    if os.path.isdir("./github_clone"):
        ssh_cmd = 'ssh -i ../key_file'
        os.chdir("./github_clone")
        repo = Repo("./")
        origin = repo.remotes.origin
        with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
            origin.pull()
        os.chdir("../")
    else:
        ssh_cmd = 'ssh -i key_file'
        Repo.clone_from(git_source, "./github_clone", env={'GIT_SSH_COMMAND': ssh_cmd})

    return True
