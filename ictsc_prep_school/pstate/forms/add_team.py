from django import forms

from pstate.models import Team


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['team_name', 'username', 'password', 'email', 'description', 'remarks']
        exclude = ['last_login', 'first_name', 'last_name', 'date_joined', 'is_superuser', 'groups', 'user_permissions', 'is_staff']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'class': "form-control"}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'remarks': forms.Textarea(attrs={'class': "form-control"}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        team = super(TeamForm, self).save(commit=False)
        team.set_password(self.cleaned_data["password"])
        if commit:
            team.save()
        return team


class TeamUpdateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['team_name', 'username', 'email', 'description', 'remarks']
        exclude = ['password', 'last_login', 'first_name', 'last_name', 'date_joined', 'is_superuser', 'groups', 'user_permissions', 'is_staff']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': "form-control"}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'remarks': forms.Textarea(attrs={'class': "form-control"}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        team = super(TeamUpdateForm, self).save(commit=False)
        if commit:
            team.save()
        return team
