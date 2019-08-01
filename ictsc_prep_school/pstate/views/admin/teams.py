from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.teams import TeamForm, TeamUpdateForm, TeamBulkCreateForm
from pstate.models import Team, Github
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from django.http import HttpResponseRedirect
from pstate.views.admin.github import GithubRepoPullExecute

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
        github = form.cleaned_data["github"]
        res = GithubRepoPullExecute(github)

#        github = Github.objects.get(id=1)
        teams_file = github.teams_file
        project_root_path = github.project_root_path
        project_path = "./github_clone/%s" % project_root_path
    
        #teamのymlを読み込む
        import yaml
        with open( project_path + "/" + teams_file, mode="r", encoding="utf-8") as f:
            teams_file = f.read()
        teams = yaml.load(teams_file)

        #チームの作成
        for team in teams:
            team = Team(team_name=team["name"], team_number=team["number"],username="team%i" % team["number"])
            team.save()

        return HttpResponseRedirect(self.success_url)
