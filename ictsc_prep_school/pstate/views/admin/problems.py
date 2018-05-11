from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from pstate.forms.problems import ProblemForm, ProblemUpdateForm, ProblemDescriptionUpdateForm
from pstate.models import Problem
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin


class ProblemCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = 'admin_pages/problem/add.html'
    success_url = "/manage/problems/"


class ProblemListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/index.html'
    permission_required = 'user.is_staff'
    raise_exception = True


class ProblemDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/detail.html'


class ProblemUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ProblemDescriptionUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemDescriptionUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ProblemDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Problem
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/problems/'
