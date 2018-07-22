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
        terraform_file = form.save(commit=True)
        shell_script = ShellScript(name='VNCサーバ初期化用', file_name='start.sh', terraform_file=terraform_file, body=start_sh_body)
        shell_script.save()
        problem = Problem.objects.get(id=self.kwargs['pk'])
        problem.terraform_file_id = terraform_file
        problem.save()

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
    success_url = '/pstate/manage/problems/'

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
    success_url = '/pstate/manage/close_window/'


class VariableCreateView(LoginRequiredAndPermissionRequiredMixin, CreateView):
    form_class = VariableForm
    template_name = 'admin_pages/common/add.html'
    success_url = '/pstate/manage/problems/'

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
    success_url = '/pstate/manage/close_window/'
