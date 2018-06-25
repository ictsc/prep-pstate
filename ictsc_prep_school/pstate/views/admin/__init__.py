from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect


def login(request):
    return render(request, 'admin_pages/auth/login.html')


@login_required
@permission_required('user.is_staff', raise_exception=True)
def logout(request):
    return render(request, 'admin_pages/auth/logout.html')


@login_required
@permission_required('user.is_staff', raise_exception=True)
def change_password(request):
    from pstate.forms.change_password import NoOlbPasswordCheckPasswordChangeForm
    if request.method == 'POST':
        from django.contrib import messages
        form = NoOlbPasswordCheckPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
@permission_required('user.is_staff', raise_exception=True)
def change_team_password(request, pk):
    from pstate.forms.change_password import NoOlbPasswordCheckPasswordChangeForm
    if request.method == 'POST':
        from pstate.models import Team
        from django.contrib import messages
        user = Team.objects.get(id=pk)
        form = NoOlbPasswordCheckPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('pstate-manage:team-change_password', pk=pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
@permission_required('user.is_staff', raise_exception=True)
def change_participant_password(request, pk):
    from pstate.forms.change_password import NoOlbPasswordCheckPasswordChangeForm
    if request.method == 'POST':
        from django.contrib import messages
        from pstate.models import Participant
        user = Participant.objects.get(id=pk)
        form = NoOlbPasswordCheckPasswordChangeForm(user, request.POST)
        if form.is_valid():
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoOlbPasswordCheckPasswordChangeForm(request.user)
    return render(request, 'admin_pages/common/change_password.html', {
        'form': form
    })


@login_required
@permission_required('user.is_staff', raise_exception=True)
def index(request):
    return render(request, 'admin_pages/index.html')


@login_required
@permission_required('user.is_staff', raise_exception=True)
def dashboard(request):
    return render(request, 'admin_pages/dashboard.html')


def close_window(request):
    return render(request, 'admin_pages/common/close.html')


class LoginRequiredAndPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'user.is_staff'
    raise_exception = True
