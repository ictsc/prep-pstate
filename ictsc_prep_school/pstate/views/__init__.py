
def index(request):
    if request.user.is_authenticated:
        from django.shortcuts import render
        if request.user.is_staff:
            return render(request, 'admin_pages/index.html')
        else:
            return render(request, 'user_pages/index.html')
    from django.http import HttpResponseRedirect
    from django.conf import settings
    return HttpResponseRedirect(settings.LOGIN_URL)
