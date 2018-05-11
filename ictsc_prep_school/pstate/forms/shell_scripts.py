from django import forms

from terraform_manager.models import TerraformFile

from terraform_manager.models import ShellScript


class ShellScriptForm(forms.ModelForm):
    class Meta:
        model = ShellScript
        fields = ['name', 'file_name', 'body', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'file_name': forms.TextInput(attrs={'class': "form-control"}),
            'body': forms.Textarea(attrs={'id': 'text'}),
        }


class ShellScriptUpdateForm(forms.ModelForm):
    class Meta:
        model = ShellScript
        fields = ['name', 'file_name', 'body', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'file_name': forms.TextInput(attrs={'class': "form-control"}),
            'body': forms.Textarea(attrs={'id': 'text'}),
        }
