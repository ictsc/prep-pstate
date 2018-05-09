from django.contrib.auth.forms import PasswordChangeForm


class NoOlbPasswordCheckPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        # user = kwargs['user']
        super(NoOlbPasswordCheckPasswordChangeForm, self).__init__(*args, **kwargs)
        del self.fields['old_password']
