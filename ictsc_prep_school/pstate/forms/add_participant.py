from django import forms

from pstate.models import Participant


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'assign_team']
        exclude = ['last_login', 'date_joined', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'class': "form-control"}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        participant = super(ParticipantForm, self).save(commit=False)
        participant.set_password(self.cleaned_data["password"])
        if commit:
            participant.save()
        return participant


class ParticipantUpdateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'username', 'email', 'assign_team']
        exclude = ['password', 'last_login', 'date_joined', 'is_superuser', 'groups', 'user_permissions',
                   'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        participant = super(ParticipantUpdateForm, self).save(commit=False)
        if commit:
            participant.save()
        return participant
