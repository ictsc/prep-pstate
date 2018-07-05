from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from pstate.forms.teams import TeamForm, TeamUpdateForm
from pstate.models import Team
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
