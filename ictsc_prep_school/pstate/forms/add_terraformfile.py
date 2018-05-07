from django import forms

from terraform_manager.models import TerraformFile


class TerraformFileForm(forms.ModelForm):
    class Meta:
        model = TerraformFile
        fields = '__all__'
