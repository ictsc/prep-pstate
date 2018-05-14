from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView

from pstate.forms.shell_scripts import ShellScriptForm, ShellScriptUpdateForm
from pstate.forms.terraform_files import TerraformFileForm, TerraformFileUpdateForm
from pstate.forms.variables import VariableForm, VariableUpdateForm
from pstate.models import Problem
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from terraform_manager.models import TerraformFile, ShellScript, Variable


class TerraformFileCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = TerraformFileForm
    template_name = 'admin_pages/terraform_file/add.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        terraform_file = form.save(commit=True)
        problem = Problem.objects.get(id=self.kwargs['pk'])
        problem.terraform_file_id = terraform_file
        problem.save()

        # VNCサーバのパスワードを問題環境作成時に自動で転送するためVNC_SERVER_PASSWORDを追加する.
        variable = Variable(key="VNC_SERVER_PASSWORD", value=None)
        variable.save()
        problem.terraform_file_id.variables.add(variable)
        problem.terraform_file_id.save()
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class TerraformFileUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = TerraformFile
    form_class = TerraformFileUpdateForm
    template_name = 'admin_pages/terraform_file/edit.html'

    def form_valid(self, form):
        form.save(commit=True)
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ShellScriptCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
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


class ShellScriptUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = ShellScript
    form_class = ShellScriptUpdateForm
    template_name = 'admin_pages/terraform_file/edit.html'

    def form_valid(self, form):
        form.save(commit=True)
        from django.http import HttpResponse
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class ShellScriptDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = ShellScript
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/close_window/'


class VariableCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = VariableForm
    template_name = 'admin_pages/common/add.html'
    success_url = '/manage/problems/'

    def form_valid(self, form):
        variable = form.save(commit=True)
        problem = Problem.objects.get(id=self.kwargs['pk'])
        problem.terraform_file_id.variables.add(variable)
        problem.terraform_file_id.save()
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class VariableUpdateView(LoginRequiredAndPermissionRequiredMixin, UpdateView):
    model = Variable
    form_class = VariableUpdateForm
    template_name = 'admin_pages/common/edit.html'

    def form_valid(self, form):
        form.save(commit=True)
        return HttpResponse('<script type="text/javascript">window.close();</script>')


class VariableDeleteView(LoginRequiredAndPermissionRequiredMixin, DeleteView):
    model = Variable
    template_name = 'admin_pages/common/delete.html'
    success_url = '/manage/close_window/'
