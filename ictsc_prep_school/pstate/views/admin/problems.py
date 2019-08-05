from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView

from pstate.forms.problems import ProblemForm, ProblemUpdateForm, ProblemDescriptionUpdateForm, \
    ProblemAllDeleteForm, ProblemBulkCreateForm
from pstate.models import Problem
from pstate.views.admin import LoginRequiredAndPermissionRequiredMixin
from django.http import HttpResponseRedirect
from pstate.views.admin.github import GithubRepoPullExecute
from terraform_manager.models import TerraformFile, Provider, ShellScript

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
        start_sh_body = """
## Change the password for ubuntu user
echo "ubuntu:@@VNC_SERVER_PASSWORD@@" | chpasswd

## disable fail2ban & network-manager
service fail2ban stop
chkconfig fail2ban off
service network-manager stop
chkconfig network-manager off

## Interface setting
echo auto eth1 >> /etc/network/interfaces
echo iface eth1 inet static >> /etc/network/interfaces
echo address 192.168.0.254 >> /etc/network/interfaces
echo netmask 255.255.255.0 >> /etc/network/interfaces

## VNC server settings
echo @@VNC_SERVER_PASSWORD@@ | vncpasswd -f > "/home/ubuntu/.vnc/passwd"
chmod 700 /home/ubuntu/.vnc/passwd
chown ubuntu:ubuntu /home/ubuntu/.vnc/passwd

systemctl daemon-reload
systemctl start vncserver@\:1.service
systemctl enable vncserver@\:1.service

## NAPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

## NAPT permanent
iptables-save > iptables.dat
echo 'iptables-restore < /root/iptables.dat' >> /etc/rc.local

service networking restart"""

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
                shell_script = ShellScript(name='VNCサーバ初期化用', file_name='start.sh', terraform_file=tf_file, body=start_sh_body)
                shell_script.save()

                problem = Problem(name=problem_name, display_name="test_display_name", terraform_file_id=tf_file)
                problem.save()

        return HttpResponseRedirect(self.success_url)
