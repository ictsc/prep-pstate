from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def login(request):
    return render(request, 'admin_pages/auth/login.html')


@login_required
def index(request):
    return render(request, 'admin_pages/index.html')
