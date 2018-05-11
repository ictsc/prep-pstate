from django import forms

from terraform_manager.models import TerraformFile


class TerraformFileForm(forms.ModelForm):
    class Meta:
        model = TerraformFile
        fields = ['name', 'file_name', 'provider', 'body', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'file_name': forms.TextInput(attrs={'class': "form-control"}),
            'body': forms.Textarea(attrs={'id': 'text'}),
        }


class TerraformFileUpdateForm(forms.ModelForm):
    class Meta:
        model = TerraformFile
        fields = ['name', 'file_name', 'body', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'file_name': forms.TextInput(attrs={'class': "form-control"}),
            'body': forms.Textarea(attrs={'id': 'text'}),
        }
