from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.problems import ProblemForm, ProblemUpdateForm, ProblemDescriptionUpdateForm, \
    ProblemAllDeleteForm, ProblemBulkCreateForm
from pstate.models import Problem
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from django.http import HttpResponseRedirect

class ProblemCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = 'admin_pages/problem/add.html'
    success_url = "/pstate/manage/problems/"


class ProblemListView(LoginRequiredAndPermissionRequiredMixin, ListView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/index.html'
    permission_required = 'user.is_staff'
    raise_exception = True

    def get_queryset(self):
        return super().get_queryset().order_by('id')


class ProblemDetailView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Problem
    paginate_by = 100
    template_name = 'admin_pages/problem/detail.html'


class ProblemUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/problems/'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ProblemDescriptionUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemDescriptionUpdateForm
    template_name = 'admin_pages/common/edit.html'
    success_url = '/pstate/manage/problems/'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ProblemDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Problem
    template_name = 'admin_pages/common/delete.html'
    success_url = '/pstate/manage/problems/'


class ProblemPreviewView(LoginRequiredAndPermissionRequiredMixin, DetailView):
    model = Problem
    template_name = 'admin_pages/problem/preview.html'

class ProblemAllDeleteView(LoginRequiredAndPermissionRequiredMixin, FormView):
    form_class = ProblemAllDeleteForm
    template_name = 'admin_pages/problem/all-problem-delete.html'
    success_url = '/pstate/manage/problems/'

    def form_valid(self, form):
        Problem.objects.all().delete()
        return HttpResponseRedirect(self.success_url)

class ProblemBulkCreateView(LoginRequiredAndPermissionRequiredMixin, FormView):
    form_class = ProblemBulkCreateForm
    template_name = 'admin_pages/problem/bulk-add.html'
    success_url = '/pstate/manage/problems/'

    def form_valid(self, form):
        return HttpResponseRedirect(self.success_url)

