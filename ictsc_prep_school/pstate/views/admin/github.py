from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from pstate.forms.github import GithubForm
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from pstate.models import Github


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
    fields = '__all__'
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/setting/github/'


class GithubDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Github
    template_name = 'admin_pages/setting/github/delete.html'
    success_url = '/pstate/manage/setting/github/'

