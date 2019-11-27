from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.problems import ProblemForm, ProblemUpdateForm, ProblemDescriptionUpdateForm, \
    ProblemAllDeleteForm, ProblemBulkCreateForm
from pstate.models import Problem
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from django.http import HttpResponseRedirect
from pstate.views.admin.github import GithubRepoPullExecute
from terraform_manager.models import TerraformFile, Provider, ShellScript, FileTemplate

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

        github = form.cleaned_data["github"]
        provider = form.cleaned_data["provider"]
        res = GithubRepoPullExecute(github)

        #ex) problem_list_path = "./github_clone/ictsc2019/q1"
        problem_list_path = "./github_clone/%s/%s" % (github.project_root_path, github.problem_path) 

        import glob, os        
        problems = glob.glob(problem_list_path + "/**/")

        #問題コードのディレクトリを中身を見ていく
        for problem in problems:
            #main.tfが存在していたら問題の追加を行う
            if os.path.exists(problem + "/main.tf") == True:
                with open(problem + "/main.tf", mode="r", encoding="utf-8") as f:
                    body = f.read()
                problem_name = problem.split("/")[-2]
                tf_file = TerraformFile(name="main", body=body, file_name="main.tf", provider=provider)
                tf_file.save()

                # start.shがgitに存在している場合はそれを使う
                if os.path.exists(problem + "/start.sh"):
                    with open(problem + "/start.tf", mode="r", encoding="utf-8") as f:
                        body = f.read()
                        shell_script = ShellScript(name="VNCサーバ初期化用",
                                                   file_name="start.sh",
                                                   terraform_file=tf_file,
                                                   body=body)
                else:   # 存在していない場合はテンプレートを使う
                    file_template = FileTemplate.objects.get(file_name='start.sh')
                    shell_script = ShellScript(name=file_template.name,
                                               file_name=file_template.file_name,
                                               terraform_file=tf_file,
                                               body=file_template.body)
                shell_script.save()
                problem = Problem(name=problem_name, display_name="test_display_name", terraform_file_id=tf_file)
                problem.save()

        return HttpResponseRedirect(self.success_url)
