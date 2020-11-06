from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as A_U

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else :
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwarge):
            group =None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwarge)

            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator


def adminonly(view_func):
    def wrapper_func(request, *args, **kwarge):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'user':
            return redirect('user', str(request.user))

        if group == 'admin':
            return view_func(request, *args, *kwarge)

        if group == 'blocked user':
            return HttpResponse("<h3>your account was blocked by Admin.. Please contact Administrator.....</h3><br><br>Ajamtha block galakin denne umbata.  : )")

    return wrapper_func

def useronly(view_func):
    def wrapper_func(request, *args, **kwarge):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admin':
            return redirect('admin',request.user)

        if group == 'user':
            return view_func(request, *args, *kwarge)

    return wrapper_func
